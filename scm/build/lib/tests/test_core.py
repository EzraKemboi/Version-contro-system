import os
import unittest
from myscm.core import init_repo, stage_file, commit, log, create_branch, switch_branch, merge, diff

class TestCore(unittest.TestCase):
    def setUp(self):
        """Set up a temporary repository for testing."""
        self.repo_name = "test_repo"
        os.mkdir(self.repo_name)
        os.chdir(self.repo_name)
        init_repo()

    def tearDown(self):
        """Clean up the temporary repository."""
        os.chdir("..")
        for root, dirs, files in os.walk(self.repo_name, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.repo_name)

    def test_init_repo(self):
        """Test initializing a repository."""
        self.assertTrue(os.path.exists(".myscm"))
        self.assertTrue(os.path.exists(".myscm/HEAD"))
        self.assertTrue(os.path.exists(".myscm/index"))
        self.assertTrue(os.path.exists(".myscm/refs/heads"))
        self.assertTrue(os.path.exists(".myscm/objects"))

    def test_stage_file(self):
        """Test staging a file."""
        with open("file.txt", "w") as f:
            f.write("Hello, SCM!")
        stage_file("file.txt")
        with open(".myscm/index", "r") as f:
            index_content = f.read()
        self.assertIn("file.txt", index_content)

    def test_commit(self):
        init_repo()
        stage_file("file.txt")
        commit("Initial commit")

        head_ref = open(".myscm/HEAD").read().strip()
        print(f"Test HEAD points to: {head_ref}")

        commit_path = f".myscm/objects/{head_ref}"
        self.assertTrue(os.path.exists(commit_path), 
                        f"Expected commit file not found at {commit_path}.")


    def test_create_branch(self):
        """Test creating a branch."""
        create_branch("new-branch")
        self.assertTrue(os.path.exists(".myscm/refs/heads/new-branch"))

    def test_switch_branch(self):
        """Test switching branches."""
        create_branch("new-branch")
        switch_branch("new-branch")
        with open(".myscm/HEAD", "r") as f:
            head_content = f.read().strip()
        self.assertIn("new-branch", head_content)

    def test_merge(self):
        """Test merging branches."""
        with open("file.txt", "w") as f:
            f.write("Branch content!")
        stage_file("file.txt")
        commit("Commit on main")
        create_branch("feature-branch")
        switch_branch("feature-branch")
        with open("file2.txt", "w") as f:
            f.write("Feature content!")
        stage_file("file2.txt")
        commit("Commit on feature branch")
        switch_branch("main")
        merge("feature-branch")
        self.assertTrue(os.path.exists("file2.txt"))

if __name__ == "__main__":
    unittest.main()
