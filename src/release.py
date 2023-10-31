import git

# クローンするディレクトリのパス
clone_dir = '/Users/yonekuramiki/Desktop/resarch/searchSATD-underCode/clone-release'

# リポジトリをクローンする
#repo = git.Repo.clone_from('https://github.com/mikiyonekura/chervil-hp.git', clone_dir)
repo = git.Repo.clone_from('https://github.com/apache/ant.git', clone_dir)


tags = repo.tags
for tag in tags:
    print(tag.name)

#一時的に追加
repo.git.checkout('rel/1.7.0')