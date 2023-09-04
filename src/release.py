import git

# クローンするディレクトリのパス
clone_dir = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/clone_release'

# リポジトリをクローンする
#repo = git.Repo.clone_from('https://github.com/mikiyonekura/chervil-hp.git', clone_dir)
repo = git.Repo.clone_from('https://github.com/jfree/jfreechart.git', clone_dir)

tags = repo.tags
for tag in tags:
    print(tag.name)