import songDownloader
import wx

playlistString = ""
searchString = ""
maxResults = 5

class openSearchDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(openSearchDialog, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.search = wx.StaticText(self, label = "Search string: ")
        hSizer.Add(self.search)
        
        self.textInput = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT, self.QueryChange, self.textInput)
        hSizer.Add(self.textInput)

        self.maxResults = wx.StaticText(self, label = "Max Results: ")
        hSizer.Add(self.maxResults)
        
        self.maxInput = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT, self.MaxChange, self.maxInput)
        hSizer.Add(self.maxInput)

        self.okButton = wx.Button(self, label = "Search and Download!")
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.okButton)
        
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.okButton, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

        self.SetSize((390, 100))
        self.SetTitle("Search for a song")

    def QueryChange(self, event):
        global searchString
        searchString = event.GetString()

    def MaxChange(self, event):
        global maxResults
        maxResults = event.GetString()
        
    def OnClose(self, event):
        global searchString
        global maxResults
        songDownloader.init()
        songDownloader.searchVideos(searchString, maxResults)
        self.Destroy()

class openPlaylistDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(openPlaylistDialog, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info = wx.StaticText(self, label = "Input: ")
        hSizer.Add(self.info)
        
        self.textInput = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT, self.OnChange, self.textInput)
        hSizer.Add(self.textInput)

        self.okButton = wx.Button(self, label = "Open Playlist")
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.okButton)
        
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.okButton, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

        self.SetSize((200, 100))
        self.SetTitle("Input playlist URL")

    def OnChange(self, event):
        global playlistString
        playlistString = event.GetString()
    def OnClose(self, event):
        global playlistString
        songDownloader.init()
        songDownloader.downloadPlaylist(playlistString)
        self.Destroy()
        
class MainPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap = 5, vgap = 5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.logger = wx.TextCtrl(self, size = (200, 300), style = wx.TE_MULTILINE | wx.TE_READONLY)

        self.playlistButton = wx.Button(self, label = "Download a playlist")
        self.Bind(wx.EVT_BUTTON, self.OpenPlaylist, self.playlistButton)
        
        self.songButton = wx.Button(self, label = "Search for a song")
        self.Bind(wx.EVT_BUTTON, self.search, self.songButton)

        self.metaButton = wx.Button(self, label = "Add Metadata")
        self.Bind(wx.EVT_BUTTON, self.addMetadata, self.metaButton)

        vSizer.Add(self.playlistButton)
        vSizer.Add(self.songButton)
        vSizer.Add(self.metaButton)
        
        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        hSizer.Add(vSizer, 0, wx.ALL, 5)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)
        
    def OpenPlaylist(self, event):
        self.logger.AppendText("Playlist Open\n")
        dialog = openPlaylistDialog(None, title = "Input playlist URL")
        dialog.ShowModal()
        dialog.Destroy()
        
    def search(self, event):
        self.logger.AppendText("Search Open\n")
        dialog = openSearchDialog(None, title = "Input playlist URL")
        dialog.ShowModal()
        dialog.Destroy()

    def addMetadata(self, event):
        songDownloader.organizeMusic()

#app = wx.App(redirect = 1, filename = "errorLog.txt")
app = wx.App(None)
frame = wx.Frame(None, wx.ID_ANY, "Title")
panel = MainPanel(frame)
frame.Show()
app.MainLoop()
