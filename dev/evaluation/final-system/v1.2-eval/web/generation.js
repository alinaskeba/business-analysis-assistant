// At most two RACI attempts per revision; action() returns false on a rejected request.
async function generateWithOneRepair(action, getState, report) {
    const session = getState().session;
    const pending = session?.generation_progress;
    if (pending?.raci_attempts >= 2) return false;
    const mode = session?.approval ? 'generate' : 'approve_generate';
    if (!await action(mode, pending ? 'RACI attempt 2 of 2...' : 'Generating work plan, then RACI attempt 1 of 2...')) return false;
    const progress = getState().session?.generation_progress;
    if (progress?.status === 'raci_failed' && progress.raci_attempts === 1) {
        report('First RACI attempt failed. Retrying RACI once with the validation errors...');
        await new Promise(resolve => setTimeout(resolve, 250));
        return action('generate', 'First RACI attempt failed. Running attempt 2 of 2...');
    }
    return true;
}
if (typeof module !== 'undefined') module.exports = {generateWithOneRepair};
