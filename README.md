# atompages

### Create simple static websites using Markdown, Python and Jinja 

Fed up with nodejs based projects using millions of dependencies? Just want a simple website builder with markdown and templating support? I wrote this website generator because many of the existing solutions were unnessesarily complex and hard to learn with too many dependencies. This website generator is very simple, yet powerful. Take a look inside the code, it isn't much and you'll quickly understand how to use it.

### Features:

- #### File and Folder based Simplicity
 
  Your files and folders directly translate into your website. Files are pages, folders are menu entries. It's that simple.


- #### Markdown

  Simply write your pages in Markdown syntax. The pages get inserted into the base Jinja template and converted to HTML.
  Markdown plugins are also supported.  

- #### Jinja

  The Jinja templating system can be used to extend the layout of your website or insert content from other resources. 

- #### Plugins

  Plugins are just python files which you put in a plugins subfolder "post_processors" or "pre_processors" or "global_variables". It allows you to aquire or generate content and use it to generate your pages. 
  
- #### Easy Development
  Integrated Webserver and autocompiler

### Basics:

- #### install:

  ``pip install git+https://github.com/dominikandreas/atompages.git``
  
- #### run:
  - Create a folder for your website or move to an existing folder and execute:
  
    ``atompages init``
    
    Take a look at the resulting folder structure, it's quite self explanatory
    
- #### develop:
  - Move to the root of your website and execute:
  
    ``atompages develop``
    
    This will:
      - start a webserver for the output folder
      - open a webbrowser with the correct address
      - automatically generate your website when things change
