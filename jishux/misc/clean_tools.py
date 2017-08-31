#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/29
import re
from urllib.parse import urlsplit


def clean_tags(item):
    '''
    加工标签
    '''
    content_html = item['content_html'].strip()
    # nofollow
    content_html = content_html.replace('<a', '<a rel="nofollow"')
    # TODO 空白符的处理
    # 1. 提取代码出来
    # pres = re.findall(r'<pre.*?</pre>', content_html)
    # for index, pre in enumerate(pres):
    #     content_html = content_html.replace(pre, '<pre>' + str(index) + '</pre>')
    # # 2. 去空白符
    # content_html = content_html.strip().replace('\r', '').replace('\n', '').replace('\t', '')
    # # 3. 代码还原回去
    # for index, pre in enumerate(pres):
    #     content_html = content_html.replace('<pre>' + str(index) + '</pre>', pre)
    #
    # p1 = re.compile('<p>(\s*|<br>|<br/>|&nbsp;)</p>')
    # content_html = re.sub(p1, '', content_html)
    # 去掉标签和标签之间多余的空白符号
    p2 = re.compile('>\s+<')
    content_html = re.sub(p2, '><', content_html)
    # TODO: 代码标签统一处理
    # 把img标签里面的懒加载的data-src，换成src
    content_html = content_html.replace('data-src=', 'src=')
    # 赋值
    item['content_html'] = content_html
    return item


def clean_ads(item):
    '''
    清洗广告
    '''
    # TODO 清洗广告
    return item




str = '''
<div class="markdown-body">
          <p><strong>These instructions apply to v4 and up. If you are looking for instructions for older version, please see the <a href="http://alexgorbatchev.com/SyntaxHighlighter">original manual</a>.</strong></p>
<p><img class="emoji" title=":moneybag:" alt=":moneybag:" src="https://camo.githubusercontent.com/8e1f67958831d1911267871fdb0d48675dbd7dfe/68747470733a2f2f6173736574732d63646e2e6769746875622e636f6d2f696d616765732f69636f6e732f656d6f6a692f756e69636f64652f31663462302e706e67" height="20" width="20" align="absmiddle" data-canonical-src="https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b0.png"> <img class="emoji" title=":moneybag:" alt=":moneybag:" src="https://camo.githubusercontent.com/8e1f67958831d1911267871fdb0d48675dbd7dfe/68747470733a2f2f6173736574732d63646e2e6769746875622e636f6d2f696d616765732f69636f6e732f656d6f6a692f756e69636f64652f31663462302e706e67" height="20" width="20" align="absmiddle" data-canonical-src="https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b0.png"> <img class="emoji" title=":moneybag:" alt=":moneybag:" src="https://camo.githubusercontent.com/8e1f67958831d1911267871fdb0d48675dbd7dfe/68747470733a2f2f6173736574732d63646e2e6769746875622e636f6d2f696d616765732f69636f6e732f656d6f6a692f756e69636f64652f31663462302e706e67" height="20" width="20" align="absmiddle" data-canonical-src="https://assets-cdn.github.com/images/icons/emoji/unicode/1f4b0.png"> <strong>Please <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&amp;hosted_button_id=2930402">click here to donate via PayPal</a> and just like they say on TV – give generously! It motivates me to keep working on this (12 years now and counting).</strong></p>
<p>SyntaxHighlighter lets you build a single <code>.js</code> file that will include the core, CSS theme and the syntaxes that you wish to use. The process is very simple and consists of just a few steps.</p>
<h1>
<a id="user-content-project-setup" class="anchor" href="#project-setup" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Project Setup</h1>
<pre><code>$ git clone https://github.com/syntaxhighlighter/syntaxhighlighter.git
$ cd syntaxhighlighter
$ npm install
</code></pre>
<p>There's a small number of build commands that is available:</p>
<pre><code>$ ./node_modules/gulp/bin/gulp.js --help

Usage
  gulp [TASK] [OPTIONS...]

Available tasks
  build                                         Builds distribution files to be used via `&lt;script/&gt;` tags. $ gulp build --brushes value1,value2 --theme value
  help                                          Display this help text.
  setup-project                                 Sets up project for development. RUN THIS FIRST!
  setup-project:clone-repos                     Clones all repositories from SyntaxHighlighter GitHub organization
  setup-project:link-node_modules-into-repos    Links `./node_modules` into every cloned repository
  setup-project:link-repos-into-node_modules    Links every cloned repository into `./node_modules`
  setup-project:unlink-repos-from-node_modules  Unlinks every cloned repository from `./node_modules`
</code></pre>
<p><strong>Use the <code>./node_modules/gulp/bin/gulp.js setup-project</code> command to set up the project.</strong> This will clone ALL of the repositories from <a href="https://github.com/syntaxhighlighter">https://github.com/syntaxhighlighter</a> and place them into the <code>repos</code> subfolder. You are now ready to build your own distribution file.</p>
<h1>
<a id="user-content-building-syntaxhighlighterjs" class="anchor" href="#building-syntaxhighlighterjs" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Building <code>syntaxhighlighter.js</code>
</h1>
<p>By running <code>./node_modules/gulp/bin/gulp.js build</code> you will make <code>syntaxhighlighter.js</code>, <code>theme.css</code>, and associated files. Note that the options <code>--brushes</code> and <code>--theme</code> <strong>do not</strong> have default values. If you will not specify them, you will get a script that doesn't do any syntax highlighting on its own, and you will not get the CSS file.</p>
<pre><code>$ ./node_modules/gulp/bin/gulp.js build --help

Options:
  --brushes  Comma separated list of brush names or paths to be bundled.
  --theme    Name or path of the CSS theme you want to use.
  --compat   Will include v3 brush compatibility feature. See
             http://bit.ly/1KCaUq6 for complete details.
  --output   Output folder for dist files.
    [default: ".../syntaxhighlighter/dist"]
  --help     Show help                                                 [boolean]

Available brushes are "all" or applescript, as3, base, bash, coldfusion, cpp,
csharp, css, delphi, diff, erlang, groovy, haxe, java, javafx, javascript, perl,
php, plain, powershell, python, ruby, sass, scala, sql, swift, tap, typescript,
vb, xml.

You may also pass paths to brush JavaScript files and theme SASS files.
</code></pre>
<h2>
<a id="user-content---brushes" class="anchor" href="#--brushes" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>--brushes</h2>
<p><code>--brushes</code> takes a comma separated list of brushes. Here's how brush resolution works:</p>
<pre><code>--brushes=X

1. IF X = `all`
  a. BUNDLE repos/brush-*/brush.js
  b. USE_SAMPLE repos/brush-*/sample.txt
  c. STOP

2. IF EXISTS repos/brush-X/brush.js
  a. BUNDLE repos/brush-X/brush.js
  b. USE_SAMPLE repos/brush-X/sample.txt
  c. STOP

3. IF EXISTS X
  a. BUNDLE X
  b. USE_SAMPLE DIR(X) + `/sample.txt`
  c. STOP
</code></pre>
<p>Examples:</p>
<pre><code>--brushes=all
--brushes=css
--brushes=css,javascript
--brushes=./my-brush.js
--brushes=/full/path/to/my-brush.js
--brushes=/full/path/to/my-brush.js,css,javascript
</code></pre>
<h2>
<a id="user-content---theme" class="anchor" href="#--theme" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>--theme</h2>
<p><code>--theme</code> takes a single theme name. Here's how theme resolution works:</p>
<pre><code>--theme=X

1. IF EXISTS repos/theme-X/theme.scss
  a. BUNDLE repos/theme-X/theme.scss
  b. STOP

1. IF EXISTS X
  a. BUNDLE X
  b. STOP
</code></pre>
<p>Examples:</p>
<pre><code>--theme=default
--theme=./my-theme.scss
--theme=/full/path/to/my-theme.scss
</code></pre>
<h2>
<a id="user-content---output" class="anchor" href="#--output" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>--output</h2>
<p>By default all build files are places into the <code>./dist</code> folder. You can change that by supplying this option.</p>
<h2>
<a id="user-content---compat" class="anchor" href="#--compat" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>--compat</h2>
<p>Specifying this flag will make SyntaxHighlighter v4 work with all existing v3 brushes out of the box, without bundling. See <a class="internal present" href="/syntaxhighlighter/syntaxhighlighter/wiki/Migration-Guide">Migration Guide</a> for more details</p>

        </div>
'''



