/**
 * Backup utility for creating safety copies before migration
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Create backup of source directory
 */
async function createBackup(sourceDir, backupDir) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  const backupPath = path.join(backupDir, `backup-${timestamp}`);

  // Create backup directory
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }

  // Use git to create backup if in a git repo
  try {
    // Check if git is available and we're in a repo
    execSync('git rev-parse --git-dir', { stdio: 'ignore' });

    // Create git commit as backup
    try {
      execSync('git add data/exercises/', { stdio: 'ignore' });
      execSync(`git commit -m "Pre-migration backup: ${timestamp}"`, { stdio: 'ignore' });
      console.log('  ✅ Git commit created as backup');
    } catch (e) {
      // No changes to commit, that's fine
      console.log('  ℹ️  No git changes to backup');
    }
  } catch (e) {
    // Not in a git repo, do manual backup
    console.log('  ℹ️  Not in git repo, creating manual backup...');
  }

  // Also create a manual copy
  copyDirectory(sourceDir, backupPath);
  console.log(`  ✅ Backup created at: ${backupPath}`);

  return backupPath;
}

/**
 * Recursively copy directory
 */
function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

module.exports = {
  createBackup,
};
