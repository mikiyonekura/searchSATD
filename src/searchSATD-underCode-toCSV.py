import git
import os
import difflib
import concurrent.futures
#コマンド
#time pypy3 src/searchSATD-underCode-toCSV.py &> output.log


clone_dir = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/clone'
repo_url = 'https://github.com/argouml-tigris-org/argouml.git'

global_count = 0
binary_extensions = [".java"]

def process_file(filepath, search_string, sim):
    local_count = 0
    result_dict = None
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
        for line_no, line in enumerate(lines, 1):
            line = line.strip()
            line = line.replace(" ", "")
            similarity = difflib.SequenceMatcher(None, search_string, line).ratio()
            if search_string == line or search_string in line:

                for sub_line in lines[line_no:]:
                    if sub_line.strip():
                        local_count += 1
                        result_dict = {
                            "count": local_count,
                            "result": sub_line.strip(),
                            "line_no": line_no,
                            "similarity": similarity,
                            "filepath": filepath
                        }

                        
                        print("predict_string:\n", line, "\n")
                        print("line_no || similarity \n")
                        print(line_no, "||", similarity, "\n")
                        print("filepath:\n", filepath, "\n")


                        return result_dict
            elif (line in search_string) and len(line) > 10:
        
                for sub_line in lines[line_no:]:
                    #文字列の先頭付近を少し削除(//などの除去に対応するため)
                    
                    origin_sub_line = sub_line.strip()
                    sub_line = sub_line.strip()
                    sub_line = sub_line.replace(" ", "")

                    print("sub_line:\n", sub_line, "\n")
                    #文字列の先頭付近を少し削除(//などの除去に対応するため)
                    sub_line = sub_line[4:]
                    print("frontremoved_sub_line:\n", sub_line, "\n")


                    if sub_line.strip() and not(sub_line in search_string):

                        local_count += 1
                        result_dict = {
                            "count": local_count,
                            "result": origin_sub_line,
                            "line_no": line_no,
                            "similarity": similarity,
                            "filepath": filepath
                        }
                        
                        
                        print("predict_string_new:\n", line, "\n")
                        print("line_no || similarity \n")
                        print(line_no, "||", similarity, "\n")
                        print("filepath:\n  ", filepath, "\n")


                        return result_dict
                    
    return {"count": local_count}

def search_files(search_string, sim):
    total_count = 0
    found_result = None

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(clone_dir):
            for fname in files:
                if os.path.splitext(fname)[1].lower() in binary_extensions:
                    filepath = os.path.join(root, fname)
                    result = list(executor.map(process_file, [filepath], [search_string], [sim]))
                    for res_dict in result:
                        total_count += res_dict.get("count", 0)
                        if "result" in res_dict:
                            return res_dict
    return {"count": total_count}

if __name__ == '__main__':
    if not os.path.exists(os.path.join(clone_dir, '.git')):
        git.Repo.clone_from(repo_url, clone_dir)

    repo = git.Repo(clone_dir)
    repo.git.checkout('VERSION_0_34')

    ans = []

    with open('/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/datasetNew/data--ArgoUML.txt', 'r') as f:
        count = 0

        for line in f:
            origin_search_string = line.strip()
            search_string = line.strip()
            search_string = search_string.replace(" ", "")
            count += 1

            # if count <= 1000:
            #     continue

            # if count > 5:
            #     break

            print(f"\nーーーーーーーーSearch the target string{count}ーーーーーーーーーーーーーーー\n ")
            print(f"search_string:\n {search_string}\n ")

            # if len(search_string) > 200:
            #     sim = 0.6
            #     result = "too long."
            #     ans.append((origin_search_string, result, 0, 0, 0))
            #     print(f"under_code:\n{result}\n ")
            #     res_dict = {"count": 0}
            # else:
            #     sim = 0.85
            #     res_dict = search_files(search_string, sim)
            #     result = res_dict.get("result", None)
            #     line_no = res_dict.get("line_no", None)
            #     similarity = res_dict.get("similarity", None)
            #     filepath = res_dict.get("filepath", None)
            #     ans.append((origin_search_string, result, line_no, similarity, filepath))
            #     print(f"under_code:\n{result}\n ")

            sim = 0.85
            res_dict = search_files(search_string, sim)
            result = res_dict.get("result", None)
            line_no = res_dict.get("line_no", None)
            similarity = res_dict.get("similarity", None)
            filepath = res_dict.get("filepath", None)
            ans.append((origin_search_string, result, line_no, similarity, filepath))
            print(f"under_code:\n{result}\n ")

            global_count += res_dict.get("count", 0)

    print(f"----------結果{global_count}件ヒットしました--------------------------\n")

    with open('/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/resultNew/1-under/1-under--ArgoUML.txt', 'w') as a:
        for idx, (origin_search_string, item, line_no, similarity, filepath) in enumerate(ans):
            print(f"ans_lists{idx+1}:", item, "\n")
            a.write(str(item) + "\n")

    with open('/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/resultNew/1-under/csv/1-under--ArgoUML.csv', 'w') as b:
        b.write("search_string,predict_under_code,line_no,similarity,filepath\n")
        for idx, (origin_search_string, item, line_no, similarity, filepath) in enumerate(ans):
            #ダブルクォートで囲む
            origin_search_string = f"\"{origin_search_string}\""
            item_enclosed = f"\"{item}\""
            b.write(f"{origin_search_string},{item_enclosed},{line_no},{similarity},{filepath}\n")

