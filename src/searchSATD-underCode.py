import git
import os
import difflib
import concurrent.futures

clone_dir = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/clone'
repo_url = 'https://github.com/apache/hive.git'

global_count = 0
binary_extensions = [".java"]

def process_file(filepath, search_string, sim):
    local_count = 0
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
        for line_no, line in enumerate(lines, 1):
            line = line.strip()
            line = line.replace(" ", "")
            similarity = difflib.SequenceMatcher(None, search_string, line).ratio()
            if similarity > sim:
                for sub_line in lines[line_no:]:
                    if sub_line.strip():
                        print("predict_string:\n  ", line, "\n")
                        print("filepath:\n  ", filepath, "\n")
                        print("line_no || similarity \n")
                        print(line_no, "||", similarity, "\n")
                        local_count += 1
                        return local_count, sub_line.strip()
    return local_count, None

def search_files(search_string,sim):
    total_count = 0
    found_result = None

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(clone_dir):
            for fname in files:
                if os.path.splitext(fname)[1].lower() in binary_extensions:
                    filepath = os.path.join(root, fname)
                    result = list(executor.map(process_file, [filepath], [search_string], [sim]))
                    for count, res in result:
                        total_count += count
                        if res and not found_result:
                            found_result = res
                            return total_count, found_result
    return total_count, found_result

if __name__ == '__main__':
    if not os.path.exists(os.path.join(clone_dir, '.git')):
        git.Repo.clone_from(repo_url, clone_dir)

    repo = git.Repo(clone_dir)
    repo.git.checkout('release-3.1.2-rc0')

    ans = []

    with open('/Users/yonekuramiki/Desktop/resarch/ReviewSATD_RP/src/mygitpython/data--Hive.txt', 'r') as f:
        count = 0

        for line in f:
            search_string = line.strip()
            search_string = search_string.replace(" ", "")
            count += 1

            if count == 501:
                break

            print(f"\nーーーーーーーーSearch the target string{count}ーーーーーーーーーーーーーーー\n ")
            print(f"search_string:\n {search_string}\n ")

            if len(search_string) > 200:
                sim = 0.6
                #count_increment, result = search_files(search_string,sim)
                result = "too long."
                ans.append(result)
                print(f"under_code: {result}\n ")

            else:
                sim = 0.85
                count_increment, result = search_files(search_string,sim)
                ans.append(result)
                print(f"under_code: {result}\n ")

            global_count += count_increment

    print(f"----------結果{global_count}件ヒットしました--------------------------\n")
    with open('/Users/yonekuramiki/Desktop/resarch/ReviewSATD_RP/src/mygitpython/under--Hive.txt', 'w') as a:
        for idx, item in enumerate(ans):
            print(f"ans_lists{idx+1}:", item, "\n")
            a.write(str(item) + "\n")
