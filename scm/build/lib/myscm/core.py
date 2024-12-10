import os
import time
import shutil
import hashlib

#initialize repository(init )

def init_repo():
    repo_dir = '.myscm'
    if not os.path.exists(repo_dir):
        # Create directory structure
        os.makedirs(f'{repo_dir}/refs/heads')
        os.makedirs(f'{repo_dir}/objects')
        
        # Set the default branch
        with open(f'{repo_dir}/HEAD', 'w') as f:
            f.write('refs/heads/main')  # Default branch
        
        # Initialize the empty staging area
        with open(f'{repo_dir}/index', 'w') as f:
            f.write('')  # Empty staging area
        
        # Initialize the default branch 'main'
        with open(f'{repo_dir}/refs/heads/main', 'w') as f:
            f.write('')  # Empty commit reference for the 'main' branch
        
        print("Repository initialized!")
    else:
        print("Repository already exists.")



#Staging Files( myscm add)

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return hashlib.sha1(content).hexdigest()

def stage_file(file_path):
    repo_dir = '.myscm'
    index_path = f'{repo_dir}/index'
    obj_dir = f'{repo_dir}/objects'
    
    if not os.path.exists(repo_dir):
        print("Not a valid repository.")
        return

    file_hash = hash_file(file_path)
    with open(file_path, 'rb') as f:
        content = f.read()

    with open(f'{obj_dir}/{file_hash}', 'wb') as f:
        f.write(content)

    with open(index_path, 'a') as f:
        f.write(f'{file_path} {file_hash}\n')

    print(f"Staged {file_path}.")


#Commiting Files(commit)

def commit(message):
    repo_dir = '.myscm'
    obj_dir = f'{repo_dir}/objects'
    os.makedirs(obj_dir, exist_ok=True)  # Ensure objects directory exists

    # Read HEAD
    head_path = f'{repo_dir}/HEAD'
    if not os.path.exists(head_path):
        print("Error: HEAD file does not exist. Initialize the repository first.")
        return
    with open(head_path, 'r') as f:
        head_ref = f.read().strip()
    print(f"HEAD points to: {head_ref}")

    # Validate branch path
    branch_path = f'{repo_dir}/{head_ref}'
    if not os.path.exists(branch_path):
        print(f"Error: No branch file exists at {branch_path}.")
        return
    with open(branch_path, 'r') as f:
        parent_commit = f.read().strip() or None
    print(f"Parent commit: {parent_commit}")

    # Read index
    index_path = f'{repo_dir}/index'
    if not os.path.exists(index_path):
        print("Error: Index file does not exist. Stage files before committing.")
        return
    with open(index_path, 'r') as f:
        index_content = f.read().strip()
    if not index_content:
        print("Error: No files staged for commit.")
        return
    print(f"Staged content: {index_content}")

    # Create commit
    commit_hash = hashlib.sha1(
        (index_content + message + (parent_commit or '') + str(time.time())).encode()
    ).hexdigest()
    commit_path = os.path.join(obj_dir, commit_hash)
    with open(commit_path, 'w') as f:
        f.write(f"message: {message}\n")
        if parent_commit:
            f.write(f"parent: {parent_commit}\n")
        f.write(f"index: {index_content}\n")
    print(f"Commit hash: {commit_hash}")
    print(f"Commit saved at {commit_path}")

    # Update branch
    with open(branch_path, 'w') as f:
        f.write(commit_hash)
    print(f"Branch {head_ref} updated with commit {commit_hash}.")




#parsing commit data
def parse_commit(commit_path):
    """
    Parse a commit file into a dictionary.
    :param commit_path: Path to the commit file.
    :return: Dictionary of commit data.
    """
    commit_data = {}
    with open(commit_path, 'r') as f:
        for line in f:
            if ": " in line:  # Ensure the line contains a key-value pair
                key, value = line.strip().split(": ", 1)
                commit_data[key] = value
    return commit_data


#Parse file hashes
def parse_file_hashes(files_data):
    """
    Parses file hash information from a string into a dictionary.
    :param files_data: A string containing file-to-hash mappings (e.g., "file1.txt:hash1\nfile2.txt:hash2").
    :return: A dictionary where keys are filenames and values are their respective hashes.
    """
    file_hashes = {}
    if files_data:
        for line in files_data.splitlines():
            filename, file_hash = line.split(':', 1)
            file_hashes[filename.strip()] = file_hash.strip()
    return file_hashes

def get_commit_chain(commit, obj_dir):
    """
    Get the chain of ancestors for a given commit.
    :param commit: The commit hash to start from.
    :param obj_dir: The objects directory.
    :return: A list of ancestor commit hashes.
    """
    ancestors = []
    while commit:
        ancestors.append(commit)
        commit_path = os.path.join(obj_dir, commit)
        if os.path.exists(commit_path):
            with open(commit_path, 'r') as f:
                metadata = f.read()
            parent_line = next((line for line in metadata.splitlines() if line.startswith("parent: ")), None)
            commit = parent_line.split(": ", 1)[1] if parent_line else None
        else:
            commit = None
    return ancestors



#Viewing commit history. 
def log():
    """Display commit history for the current branch(log)
    """
    repo_dir = '.myscm'
    head_path = f'{repo_dir}/HEAD'
    obj_dir = f'{repo_dir}/objects'

    if not os.path.exists(repo_dir):
        print("Not a valid repository.")
        return

    with open(head_path, 'r') as f:
        current_branch = f.read().strip()

    branch_path = f'{repo_dir}/{current_branch}'
    if not os.path.exists(branch_path):
        print("No commits yet.")
        return

    commit_hash = open(branch_path).read().strip()
    while commit_hash:
        commit_file = f'{obj_dir}/{commit_hash}'
        with open(commit_file, 'r') as f:
            print(f.read())
        commit_hash = next((line.split(': ')[1] for line in open(commit_file).readlines() if line.startswith('parent')), None)


#Branching
def create_branch(branch_name):
    repo_dir = '.myscm'
    head_path = f'{repo_dir}/HEAD'
    refs_dir = f'{repo_dir}/refs/heads'

    if not os.path.exists(repo_dir):
        print("Not a valid repository.")
        return

    with open(head_path, 'r') as f:
        current_branch = f.read().strip()

    current_commit = open(f'{repo_dir}/{current_branch}').read().strip()
    new_branch_path = f'{refs_dir}/{branch_name}'

    with open(new_branch_path, 'w') as f:
        f.write(current_commit)

    print(f"Branch '{branch_name}' created at {current_commit}.")

def switch_branch(branch_name):
    repo_dir = '.myscm'
    refs_dir = f'{repo_dir}/refs/heads'
    head_path = f'{repo_dir}/HEAD'

    branch_path = f'{refs_dir}/{branch_name}'
    if not os.path.exists(branch_path):
        print(f"Branch '{branch_name}' does not exist.")
        return

    with open(head_path, 'w') as f:
        f.write(f'refs/heads/{branch_name}')

    print(f"Switched to branch '{branch_name}'.")

#Merging files
def merge(branch_name):
    repo_dir = '.myscm'
    refs_dir = f'{repo_dir}/refs/heads'
    obj_dir = f'{repo_dir}/objects'
    head_path = f'{repo_dir}/HEAD'

    if not os.path.exists(repo_dir):
        print("Not a valid repository.")
        return

    # Current branch and target branch
    with open(head_path, 'r') as f:
        current_branch = f.read().strip()
    target_branch_path = f'{refs_dir}/{branch_name}'

    if not os.path.exists(target_branch_path):
        print(f"Branch '{branch_name}' does not exist.")
        return

    current_commit = open(f'{repo_dir}/{current_branch}').read().strip()
    target_commit = open(target_branch_path).read().strip()

    # Traverse history to find common ancestor (simplified linear history here)
    ancestor = find_common_ancestor(current_commit, target_commit, obj_dir)  # Verify this function works
    if ancestor is None:
        raise ValueError("No common ancestor found between the branches.")  # Add this for debugging

    # Diff current and target commits relative to ancestor
    current_changes = get_diff(ancestor, current_commit, obj_dir)
    target_changes = get_diff(ancestor, target_commit, obj_dir)

    # Check for conflicts
    conflicts = []
    for file, hash in target_changes.items():
        if file in current_changes and current_changes[file] != hash:
            conflicts.append(file)

    if conflicts:
        print(f"Merge conflict detected in: {', '.join(conflicts)}")
        return

    # Apply non-conflicting changes
    for file, hash in target_changes.items():
        if file not in current_changes:
            stage_file(file)  # Reuse stage logic

    print(f"Merge of branch '{branch_name}' into '{current_branch}' completed.")

def find_common_ancestor(commit1, commit2, obj_dir):
    """Traverse parent chains to find the first common commit."""
    ancestors1 = get_commit_chain(commit1, obj_dir)
    ancestors2 = get_commit_chain(commit2, obj_dir)
    return next((commit for commit in ancestors1 if commit in ancestors2), None)

def get_diff(ancestor, commit, obj_dir):
    """Compare two commits and return changed files."""
    ancestor_data = parse_commit(f'{obj_dir}/{ancestor}')
    commit_data = parse_commit(f'{obj_dir}/{commit}')
    ancestor_files = parse_file_hashes(ancestor_data.get('files', ''))
    commit_files = parse_file_hashes(commit_data.get('files', ''))
    return {file: commit_files[file] for file in commit_files if commit_files.get(file) != ancestor_files.get(file)}

#Diff
def diff(commit1, commit2):
    repo_dir = '.myscm'
    obj_dir = f'{repo_dir}/objects'

    data1 = parse_commit(f'{obj_dir}/{commit1}')
    data2 = parse_commit(f'{obj_dir}/{commit2}')

    files1 = parse_file_hashes(data1['files'])
    files2 = parse_file_hashes(data2['files'])

    for file in set(files1.keys()).union(files2.keys()):
        hash1 = files1.get(file)
        hash2 = files2.get(file)

        if hash1 != hash2:
            print(f"File: {file}")
            if hash1:
                print("Old:")
                print(open(f'{obj_dir}/{hash1}', 'r').read())
            if hash2:
                print("New:")
                print(open(f'{obj_dir}/{hash2}', 'r').read())

#Ignoring files
def should_ignore(file_path):
    ignore_file = '.myscmignore'
    if not os.path.exists(ignore_file):
        return False
    with open(ignore_file, 'r') as f:
        ignored_patterns = f.read().splitlines()
    return any(file_path.endswith(pattern) for pattern in ignored_patterns)

#Cloning repository
def clone_repo(source, destination):
    if not os.path.exists(f'{source}/.myscm'):
        print("Source is not a valid repository.")
        return
    shutil.copytree(f'{source}/.myscm', f'{destination}/.myscm')
    print(f"Repository cloned to {destination}.")
