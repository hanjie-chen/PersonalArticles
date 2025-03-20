# Flask Command

对于需要应用上下文(Application Context)的 Flask CLI 命令，你实际上不需要先运行 `flask run`。Flask CLI 命令在执行时会自动创建一个应用上下文。

不过，你的代码中有几个地方需要注意和改进：

1. **命令定义的最佳实践**
```python
# 推荐的方式
import click
from flask.cli import with_appcontext

@click.command('import_articles')
@with_appcontext  # 显式声明需要应用上下文
def import_articles_command():
    import_articles()
    
# 注册命令
app.cli.add_command(import_articles_command)
```

2. **避免循环导入**
你的代码可能会遇到循环导入的问题，建议重构如下：

```python
# commands.py
import click
from flask.cli import with_appcontext
from models import db, Article_Meta_Data
import os
import frontmatter
import re
from datetime import date

Articles_Directory = "/home/Plain/Personal_Project/Test_Articles_Data"

@click.command('import_articles')
@with_appcontext
def import_articles_command():
    # 获取所有.md files
    md_files = [f for f in os.listdir(Articles_Directory) if f.endswith('.md')]

    for md_file in md_files:
        try:
            process_article(md_file)
        except Exception as e:
            click.echo(f"Error processing {md_file}: {str(e)}")
            continue

    db.session.commit()
    click.echo("All articles have been imported.")

def process_article(md_file):
    md_path = os.path.join(Articles_Directory, md_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        article = f.read()
    
    # 分割文件内容
    split = article.split('<!-- split -->', 1)
    if len(split) != 2:
        click.echo(f"File: {md_file} lacks <!-- split -->, skipped")
        return
    
    metadata_part, body_part = split
    
    # 解析元数据
    post = frontmatter.loads(metadata_part)
    metadata = post.metadata
    left_content = post.content

    # 提取简介
    brief_intro_text = extract_brief_introduction(left_content, md_file)
    
    # 获取文件修改时间
    file_stat = os.stat(md_path)
    file_last_modified_time = date.fromtimestamp(file_stat.st_mtime)

    # 创建数据库实例
    article_metadata = create_article_metadata(
        metadata, 
        file_last_modified_time, 
        brief_intro_text
    )

    # 检查重复
    if check_duplicate_article(article_metadata.title):
        click.echo(f'Article {article_metadata.title} exists in database, skipped')
        return

    db.session.add(article_metadata)
    click.echo(f'Article {article_metadata.title} added')

def extract_brief_introduction(content, filename):
    brief_intro_pattern = re.compile(r'```.*?BriefIntroduction:\s*(.*?)```', re.DOTALL)
    brief_intro_match = brief_intro_pattern.search(content)
    if brief_intro_match:
        return brief_intro_match.group(1).strip()
    click.echo(f"Failed to parse BriefIntroduction in {filename}")
    return ''

def create_article_metadata(metadata, modified_time, brief_intro):
    return Article_Meta_Data(
        title=metadata.get('Title', 'Untitled'),
        author=metadata.get('Author', 'Plain'),
        instructor=metadata.get('Instructor'),
        cover_image_url=metadata.get('CoverImage', 'unknown'),
        rollout_date=date.fromisoformat(metadata.get('RolloutDate')),
        category=metadata.get('Category', 'unclassified'),
        ultimate_modified_date=modified_time,
        brief_introduction=brief_intro
    )

def check_duplicate_article(title):
    result = db.session.execute(
        db.select(Article_Meta_Data)
        .where(Article_Meta_Data.title == title)
    ).first()
    return result is not None
```

3. **在主应用中注册命令**
```python
# app.py
from flask import Flask
from commands import import_articles_command

app = Flask(__name__)
# ... 其他配置 ...

# 注册命令
app.cli.add_command(import_articles_command)
```

4. **使用方法**
```bash
# 直接运行命令
flask import_articles

# 如果需要指定 Flask 应用
export FLASK_APP=app.py
flask import_articles

# 或者在命令行指定
FLASK_APP=app.py flask import_articles
```

5. **其他改进建议**

a) 添加进度显示：
```python
from tqdm import tqdm

@click.command('import_articles')
@with_appcontext
def import_articles_command():
    md_files = [f for f in os.listdir(Articles_Directory) if f.endswith('.md')]
    
    with tqdm(total=len(md_files)) as pbar:
        for md_file in md_files:
            process_article(md_file)
            pbar.update(1)
```

b) 添加命令选项：
```python
@click.command('import_articles')
@click.option('--directory', default=Articles_Directory, help='Articles directory path')
@click.option('--dry-run', is_flag=True, help='Show what would be done')
@with_appcontext
def import_articles_command(directory, dry_run):
    click.echo(f"Importing articles from {directory}")
    if dry_run:
        click.echo("Dry run mode - no changes will be made")
    # ... 其余代码
```

c) 添加错误处理和事务：
```python
@click.command('import_articles')
@with_appcontext
def import_articles_command():
    try:
        # ... 处理逻辑 ...
        db.session.commit()
        click.echo("Successfully imported all articles")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error occurred: {str(e)}", err=True)
        raise click.Abort()
```

使用这些改进后的代码：
- 更容易维护和测试
- 有更好的错误处理
- 提供更友好的用户界面
- 支持更多配置选项
- 避免了循环导入问题
- 正确处理应用上下文

记住，Flask CLI 命令会自动处理应用上下文，所以你不需要先运行应用就能执行这些命令。