# VOP Snippets
The purpose of this tool is to provide an easy way to store and re-use small portions of code in a VOP network.
Snippets can be created only for VOP networks, I haven't tested within the new Material context. Also, in order to preserve Houdini's EULA, snippets are not necessarily cross-license compatible and that's a feature, not an issue. For all concerns, the snippets respect the same cross-license compatibility as .hip files. Please respect this feature and support SideFX's fenomenal work. They are real people with families and with a passion for their work, which clearly translates to into the awesome tools they make available to end users.

## Installation
1) Copy the contents of ./toolbar into your toolbar folder within your Houdini preferences folder.
(e.g. Windows =>C:\Users\user\Documents\houdini16.0\toolbar)

2) Copy the contents of ./scripts into your scripts folder within your Houdini preferences folder.
(e.g. Windows => C:\Users\user\Documents\houdini16.0\scripts)

3) Lauch Houdini and on your shelf tab, add the the "VOP Snippets" tab using the menu on the right upper corner.

## Usage
There are 2 tools, one to write snippets and another to read them. In either case you need to be inside the VOP network you're trying to read/write from/to.
To write a snippet, select the nodes you want to write and click the write button. A file save dialog will pop-up and let you choose a location and file name for your snippet.
Reading a snippet is a similar process, just press the read snippet from the shelf, navigate to and select the desired snippet file and the contents will be added to your VOP network (hopefully not too far from your current position within your network editor).

## To do
I'd like to create an UI, not sure if it's necessary, maybe just to better organize the snippets and facilitate browsing.

## Bugs and feature requests
Tool is provided "as is", and although I'm usually busy, I'd be open to reading good ideas and attempting to fix some issues. Feel free to contact me, even if I can't guarantee I'll be able to respond.
