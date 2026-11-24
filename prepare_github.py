"""Build a Git-ignore-aware public archive and block configured credentials from publication."""
import json
import os
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent


def main():
    temp = ROOT / '.local-archive/publication-check'
    temp.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', str(temp)], check=True, capture_output=True)
    command = ['git', f'--git-dir={temp / ".git"}', f'--work-tree={ROOT}',
               'ls-files', '--others', '--exclude-standard', '-z']
    result = subprocess.run(command, check=True, capture_output=True)
    files = sorted(Path(name) for name in result.stdout.decode('utf-8').split('\0') if name)
    files = [name for name in files if (ROOT / name).is_file()]
    import business_analysis as ba
    ba.load_env()
    values = [os.getenv(key, '').strip().encode() for key in ('GEMINI_API_KEY', 'OPENAI_API_KEY')]
    values = [value for value in values if len(value) >= 12]
    pattern = re.compile(rb'(?:AIza[0-9A-Za-z_-]{30,}|sk-[0-9A-Za-z_-]{25,})')
    findings = []
    for name in files:
        resolved = (ROOT/name).resolve()
        if not resolved.is_relative_to(ROOT) or '..' in name.parts:
            raise ValueError('Public file is outside the workspace')
        data = resolved.read_bytes()
        if any(value in data for value in values) or pattern.search(data):
            findings.append(str(name))
        if name.suffix.lower() == '.docx':
            with ZipFile(resolved) as document:
                for member in document.namelist():
                    content = document.read(member)
                    if any(value in content for value in values) or pattern.search(content):
                        findings.append(str(name))
    if findings:
        print(json.dumps({'status':'blocked','files_with_possible_credentials':sorted(set(findings))}))
        raise SystemExit(1)
    archive = ROOT / 'github-ready.zip'
    with ZipFile(archive,'w',ZIP_DEFLATED) as package:
        for name in files:package.write(ROOT/name,name.as_posix())
    with ZipFile(archive) as package:
        assert package.testzip() is None
        assert not any(name.startswith(('sessions/','.local-archive/','submission/')) for name in package.namelist())
        assert '.env' not in package.namelist()
    audit = {'status':'passed','files':len(files),'configured_credentials_or_key_patterns':0,
             'archive':'github-ready.zip','publication':'Not uploaded; no root Git repository initialized.',
             'public_files':[str(name) for name in files]}
    (temp/'audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='public_files'}))


if __name__=='__main__':main()
