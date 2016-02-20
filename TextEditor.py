
import wx
import wx.richtext as RichText
import wx.stc as stc
import os
import random
import subprocess

class myWindow(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1585,687),pos=(-8,0))
        
        #Set Window Properties
        self.SetBackgroundColour((0,0,0))
        self.SetBackgroundStyle(2)
        
        #create panels
        self.framePanel = wx.Panel(self,-1)
        self.textPanel = self.EditorPanel(self.framePanel)
        self.sidePanel = self.RightPanel(self.framePanel)
        self.outPanel = self.OutputPanel(self.framePanel)
        
        '''NOT SURE HOW THE SIZER WORKS YET
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(self.textPanel)
        sizer.Add(self.sidePanel)
        '''
        
        self.StatusBar = self.CreateStatusBar() #create a status bar
        self.StatusBar.SetFieldsCount(2)
        self.StatusBar.SetStatusText("Line: " + str(self.textPanel.control.GetNumberOfLines()), 1)    #need method for autorefreshing panel
        
        self.toolBar = self.CreateToolBar()     #create a tool bar
        fileMenu = wx.Menu()                    #initialize a file menu
        editMenu = wx.Menu()                    #initialize an edit menu
        
        #create "file" options
        menuAbout = fileMenu.Append(wx.ID_ABOUT,"&About","Program Information")
        fileMenu.AppendSeparator()
        menuOpen = fileMenu.Append(wx.ID_OPEN,"&Open","Open a File")
        fileMenu.AppendSeparator()
        menuSave = fileMenu.Append(wx.ID_SAVE,"&Save", "Save File Contents")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT,"&Exit", "Terminate Program")
        
        #create "edit" options
        menuBold = editMenu.Append(wx.ID_BOLD,"&Bold","Set Bold Text")
        editMenu.AppendSeparator()
        menuItalic = editMenu.Append(wx.ID_ITALIC,"&Italic","Set Italic Text")
        
        #create the menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") #add file menu to menu bar
        menuBar.Append(editMenu,"&Edit") #add edit menu to menu bar
        self.SetMenuBar(menuBar)         #add menu bar to frame
    
        
        #bind event handlers for menu buttons
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)   
        
        #Fill Toolbar
        openTool = self.toolBar.AddTool(wx.ID_ANY,wx.Bitmap("open.png"))
        self.toolBar.Bind(wx.EVT_TOOL,self.OnOpen,openTool)
        saveTool = self.toolBar.AddTool(wx.ID_ANY,wx.Bitmap("save.png"))
        self.toolBar.Bind(wx.EVT_TOOL,self.OnSave,saveTool)
        findTool = self.toolBar.AddTool(wx.ID_ANY,wx.Bitmap("find.png"))
        self.toolBar.Bind(wx.EVT_TOOL,self.OnFind,findTool)
        compileTool = self.toolBar.AddTool(wx.ID_ANY,wx.Bitmap("pie.png"))
        self.toolBar.Bind(wx.EVT_TOOL,self.OnCompile,compileTool)
        self.toolBar.Realize()
        
        #event handlers for the right panel buttons
        self.sidePanel.button2.Bind(wx.EVT_BUTTON,self.OnButton2)
        
        #event handlers for the text panel control
        self.textPanel.control.Bind(wx.EVT_TEXT,self.OnTextChg)
        self.textPanel.control.Bind(wx.EVT_TEXT_ENTER,self.OnTextEnter)
        
        #dictates whether the document has been saved yet.
        self.fileExists = False
            
        self.Show(True)
        
#---------------------------------------------------------------------------------------
#Panel Classes and associated methods
#---------------------------------------------------------------------------------------
        
    class RightPanel(wx.Panel):
        
        def __init__(self,parent=-1,size=(580,577)):
            wx.Panel.__init__(self,parent=parent,id=wx.ID_ANY,size=size,pos=(1000,0))
            self.SetBackgroundColour((50,250,100))
            
            self.button1 = wx.Button(self,label="I'm a Button")
            self.button1.Bind(wx.EVT_BUTTON,self.OnButton1)
            self.button2 = wx.Button(self,label="Clear Output")
            
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.button1)
            sizer.Add(self.button2)
            self.SetSizer(sizer)
            self.Layout()
            
        def OnButton1(self,evt):
            #Pressing button1 randomly changes background colour
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            self.SetBackgroundColour((r,g,b))
            self.Refresh()
            
            
    class EditorPanel(wx.Panel):
        
        def __init__(self,parent=-1,size=(1000,400)):
            wx.Panel.__init__(self,parent=parent,id=wx.ID_ANY,size=size)
            wx.richtext.RichTextCtrl(self,size=size,pos=(20,0))
            self.control = stc.StyledTextCtrl(self,style=(wx.SIMPLE_BORDER|wx.TE_PROCESS_ENTER),size=(980,400),pos=(20,0))
            '''None of these seem to work, need to install wxWidgets?
            self.control = wx.richtext.RichTextCtrl(self,style=(wx.RE_MULTILINE),size=size,pos=(20,0))
            self.control = self.stc.StyledTextCtrl(self,style=wx.SIMPLE_BORDER,size=(980,400),pos=(20,0))
            self.control = self.StyledControl(wx.stc.StyledTextCtrl)
            '''
            #self.control = wx.TextCtrl(self,style=(wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|
                                      # wx.TE_PROCESS_TAB|wx.TE_RICH2),size=size,pos=(20,0))
            self.numbering = wx.TextCtrl(self,style=(wx.TE_READONLY|wx.TE_MULTILINE),size=(20,400))
            
            self.numbering.SetValue('1\n')
            self.control.dirty = False
            self.control.prevNumberLines = 0
      
    '''      
    class StyledControl(wx.stc.StyledTextCtrl):
        
        def __init__(self,parent=-1,style=wx.SIMPLE_BORDER,size=(980,400),pos=(20,0)):
            wx.stc.StyledTextCtrl.__init__(self,parent=parent,style=style,size=size,pos=pos)
    '''
            
    class OutputPanel(wx.Panel):
        
        def __init__(self, parent=-1,size=(1000,177)):
            wx.Panel.__init__(self,parent=parent,id=wx.ID_ANY,size=size,pos=(0,400))
            
            self.outControl = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=size)
            
        
#-------------------------------------------------------------------------------------------------   
#Main window methods
#-------------------------------------------------------------------------------------------------

    def OnAbout(self,evt):
        dlg = wx.MessageDialog(self,"This is a small text editor.", "About My Simple GUI", wx.OK)
        dlg.ShowModal()         #show the message box
        dlg.Destroy()           #close it when finished
    
    def OnOpen(self,evt):
        '''Method opens a file for editing'''
        self.dirname = ''
        dlg = wx.FileDialog(self,"Choose a File", self.dirname,"","*.*",wx.OPEN)
        dlg.SetWildcard("C Files (*.c)|*.c|TEXT Files (*.txt)|*.txt")
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.textPanel.control.SetValue(f.read())
            f.close()
            self.fileExists = True
            self.SetTitle(self.filename)
            self.textPanel.numbering.SetValue('1\n')
            for i in range(2,self.textPanel.control.GetNumberOfLines() + 1):
                self.textPanel.numbering.AppendText(str(i) + '\n')
            
        dlg.Destroy()
      
    def OnSave(self,evt):
        '''Method saves current text to file'''
        if self.fileExists == False:   #file DNE, need to do a SaveAs
            dlg = wx.FileDialog(self,"Save File","","","*.*",wx.SAVE)
            dlg.SetWildcard("C Files (*.c)|*.c|TEXT Files (*.txt)|*.txt")
            
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename),'w')
                f.write(self.textPanel.control.GetValue())
                f.close()
                self.SetTitle(self.filename)
                self.fileExists = True
                self.textPanel.control.dirty = False
                
            dlg.Destroy()
                
        else:       #file exists, save updates
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.textPanel.control.GetValue())
            f.close()
            self.SetTitle(self.filename)
            self.textPanel.control.dirty = False
            
    def OnFind(self,evt):
        #Need to open up a new message dialog to interact with
        text = self.textPanel.control.GetValue()
        
        splitText = text.split(" ,.!\'\";:")
        
    def OnTextChg(self,evt):
        #append * to filename to show that it's unsaved
        if self.textPanel.control.dirty == False:
            self.textPanel.control.dirty = True
            self.SetTitle(self.GetTitle() + '*')
        
        #upon typing, update line count
        self.StatusBar.SetStatusText("Line: " + str(self.textPanel.control.GetNumberOfLines())
        + " | Pos: " + str(self.textPanel.control.GetInsertionPoint()), 1)
      
    def OnCompile(self,evt):
        
        self.OnSave(wx.EVT_TEXT)           #save file before compiling
        
        os.chdir('C:\\cygwin64\\bin\\')
        compiler = subprocess.Popen(['gcc.exe','programs\\' + self.filename],stdin=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        (c_out,c_err) = compiler.communicate()
        
        if compiler.returncode != 0:
            self.outPanel.outControl.AppendText("Compiler ERROR:\n" + str(c_err))
        else:
            executable = subprocess.Popen('a.exe',stdout=subprocess.PIPE)
            (out,err) = executable.communicate()
            self.outPanel.outControl.AppendText(str(out))
       
    def OnTextEnter(self,evt):
        
        #when new line added, increase number of lines beside code
        if self.textPanel.control.GetNumberOfLines() > self.textPanel.control.prevNumberLines:
            self.textPanel.control.prevNumberLines += 1
            self.textPanel.numbering.AppendText(str(self.textPanel.control.prevNumberLines + 1) + '\n')

        #if last character was '{' then add 
        #line = self.textPanel.control.GetLineText()
        #below line doesn't do anything, apparently...
        self.textPanel.control.AddText("you pressed enter")
        
         
    def OnButton2(self,evt):
            self.outPanel.outControl.Clear()
        
    def OnExit(self, evt):
        self.Close(True)
    

app = wx.App(False)                  #Create a new app, don't redirect stdout/stderr
frame = myWindow(None, "-Untitled") #create a top-level window
frame.Show(True)
app.MainLoop()


