import subprocess
import os


def check_git_status():
    print("🔍 Checking Git Status...")
    print("=" * 50)

    # Check if git is initialized
    if not os.path.exists(".git"):
        print("❌ Git not initialized!")
        print("   Run: git init")
        return False

    # Get git status
    try:
        # Check branch
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Check commits
        commits = subprocess.run(
            ["git", "log", "--oneline"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Check remote
        remote = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        ).stdout.strip()

        print(f"✅ Git initialized")
        print(f"📁 Branch: {branch or 'Not set'}")

        if commits:
            print(f"📝 Commits: {len(commits.split('\\n'))}")
            print("Latest commits:")
            for line in commits.split('\\n')[:3]:
                print(f"  • {line}")
        else:
            print("📝 No commits yet")

        if remote:
            print(f"🌐 Remote: Configured")
            for line in remote.split('\\n'):
                print(f"  {line}")
        else:
            print("🌐 Remote: Not configured")

        return True

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return False


if __name__ == "__main__":
    check_git_status()