# -*- coding:utf-8 -*-
 # bissue.py
import click
import os
import tempfile
import json
import zipfile
import codecs

from datetime import datetime
appName = "bissue"
extension = ".json"
initFileName ="init"
jsonFileName = "db-1.0"
assignee = "appprino"

def getBaseDir():
    return tempfile.gettempdir()

def getProjectDir():
    return getBaseDir() +"/"+ appName +"/"

def getInitFilePath():
    return getProjectDir()+initFileName+ extension

def getProjectNameByJson():
    f = open(getInitFilePath())
    data = json.load(f)
    return data["name"].encode('utf-8')

def load():
    """一時的に保存してあるIssue情報をロード"""
    f = open(getInitFilePath())
    data = json.load(f)
    issueList = data["issueList"]
    return issueList

def save(issueList):
    """一時的にIssue情報を保存"""
    f = open(getInitFilePath())
    data = json.load(f)
    f.close()
    data["issueList"] = issueList
    with open(getInitFilePath(), 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()


def makeMeta(assignee,kind="task"):
    meta = {"default_assignee":assignee,
            "default_component":"null",
            "default_kind":kind,
            "default_milestone":"null",
            "default_version":"null"}
    return meta

def makeIssueJson(issueList,meta):
    issues = []
    now = datetime.now().isoformat()
    for issue in issueList:
        data = {}
        data["id"] = issue["id"]
        data["title"] = issue["title"]
        data["content"] = issue["content"]
        data["assignee"] = assignee
        data["kind"] = "task"
        data["priority"] = "major"
        data["status"] = "new"
        data["content_updated_on"] = now
        data["updated_on"] = now
        data["created_on"] = now
        issues.append(data)

    issueJson = """
        "issues":
            {issues}
        ,
        "meta":{meta}
    """.format(issues=issues,meta=meta).replace("\'","\"").replace("u\"","\"")
    issueJson = "{" + issueJson + "}"
    return issueJson

def addOneIssueData(title,content,id):
    issueList = load()
    # idが指定されていなかったら自動的に連番で作成する
    if id == -1:
        id = len(issueList)
    # issue情報を作成
    newIssue = {"id":id,"title":title,"content":content}
    issueList.append(newIssue)
    save(issueList)



@click.group()
def cli():
    pass

@cli.command()
@click.option("--name",type=str,default="bissueProject")
def init(name):
    """プロジェクトをセットアップ"""
    if os.path.exists(getProjectDir()) == False:
        os.mkdir(getProjectDir())
    f = open(getInitFilePath(),"w")
    template = "{\"name\":\""+name+"\",\"issueList\":[]}"
    f.write(template)
    # out put
    click.echo("{appName} - [{name}] 初期化しました".format(appName=appName.encode('utf-8'),name=name.encode('utf-8')))
    click.echo("filepath {path}".format(path=getInitFilePath().encode('utf-8')))


@cli.command()
@click.argument("title",type=str)
@click.option("--content",type=str,default="")
@click.option("--id",type=int,default=-1)
def add(title,content,id):
    """issue情報を追加"""
    addOneIssueData(title,content,id)
    click.echo("success! {title}".format(title=title.encode('utf-8')))



@cli.command()
def list():
    """issue情報を表示"""
    issueList = load()
    click.echo(" [id] - [title]")
    for issue in issueList:
        click.echo("{id:5d} - {title}".format(id=issue["id"],title=issue["title"].encode('utf-8')))


@cli.command()
def path():
    """一時ファイルpathを表示"""
    click.echo(getInitFilePath())

@cli.command()
@click.argument("id",type=int)
def delete(id):
    """登録したissueを削除"""
    issueList = load()
    isSuccess = False
    for issue in issueList:
        if issue["id"] == id:
            isSuccess = True
            issueList.remove(issue)
    save(issueList)
    if isSuccess == False:
        click.echo(" id:{id} の削除に失敗しました".format(id=id))


@cli.command()
def convert():
    """issue情報をまとめる"""
    meta = makeMeta("appprino")
    issueList = load()
    issueJson = makeIssueJson(issueList,meta)
    f = open(jsonFileName+extension,"w")
    f.write(issueJson)
    f.close()
    # zipにする
    zipfileName = getProjectNameByJson()
    zipFile = zipfile.ZipFile("bissue_{projectName}.zip".format(projectName=getProjectNameByJson()),"w",zipfile.ZIP_STORED)
    zipFile.write(jsonFileName+extension)
    click.echo("maked {fileName}.zip".format(fileName=zipfileName.encode('utf-8')))
    zipFile.close()
    os.remove(jsonFileName+extension)

@cli.command()
@click.argument("filepath",type=str)
def loadfile(filepath):
    """テキストからissue情報を保存する"""
    if os.path.exists(filepath) == False:
        raise click.BadParameter("no such file")
    f = codecs.open(filepath, 'r', "utf-8")
    line = f.readline().strip()
    while line:
        click.echo(line)
        addOneIssueData(line,"",-1)
        line = f.readline().strip()
    f.close

@cli.command()
def count():
    """一時領域に保存してあるissue情報の数を表示"""
    issueList = load()
    click.echo(len(issueList))