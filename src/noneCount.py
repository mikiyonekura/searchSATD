import os
import glob

def countNone():
    path = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/result/1-under'
    label_path = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/result/1-label'
    files = sorted(glob.glob(path + '/*.txt'))
    label_files = sorted(glob.glob(label_path + '/*.txt'))

    for file, label_file in zip(files, label_files):
        with open(file, 'r') as data_file, open(label_file, 'r') as lbl_file:
            data_lines = data_file.readlines()
            label_lines = lbl_file.readlines()
            file_counts = {'positive': 0, 'negative': 0}  # ファイルごとのNoneのカウント
            total_data = len(data_lines)

            # 各行に対してNoneのカウントを取得
            for data_line, label_line in zip(data_lines, label_lines):
                label = label_line.strip()
                count = data_line.count("None")
                file_counts[label] += count

            # ファイルとラベルごとのカウントを出力
            print(f"ファイル{os.path.basename(file)}の中に、positiveのNoneは{file_counts['positive']}個/{total_data}データ, negativeのNoneは{file_counts['negative']}個/{total_data}データあります。")

if __name__ == '__main__':
    countNone()
