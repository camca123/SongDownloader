#SongDownloader
#Written by Cameron Swinoga
#Meant to automatically search Youtube for a song, download it, and add metadata to it

import songDownloader
import wx
import file_reader
import os
#import pafy

playlistString = ""
searchString = ""
maxResults = 5

class openSearchDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(openSearchDialog, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.directory = wx.StaticText(self, label = file_reader.readFromFile("musicDirectory"))
        
        self.search = wx.StaticText(self, label = "Search string: ")
        hSizer.Add(self.search)
        
        self.textInput = wx.TextCtrl(self, size=(150, -1))
        self.Bind(wx.EVT_TEXT, self.QueryChange, self.textInput)
        hSizer.Add(self.textInput)

        hSizer.AddSpacer(10)
        
        self.maxResults = wx.StaticText(self, label = "Max Results: ")
        hSizer.Add(self.maxResults)
        
        self.maxInput = wx.TextCtrl(self, size=(30, -1))
        self.Bind(wx.EVT_TEXT, self.MaxChange, self.maxInput)
        hSizer.Add(self.maxInput)

        self.progressGauge = wx.Gauge(self, -1, 100, (100, 100), (250, 25))
        
        self.downloadButton = wx.Button(self, label = "Search and Download!")
        self.Bind(wx.EVT_BUTTON, self.OnDownload, self.downloadButton)

        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.progressGauge, 0, wx.CENTER)
        mainSizer.Add(self.directory, 0, wx.CENTER)
        mainSizer.Add(self.downloadButton, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

        self.SetSize((350, 150))
        self.SetTitle("Search for a song")
        
    
        
    def QueryChange(self, event):
        global searchString
        searchString = event.GetString()

    def MaxChange(self, event):
        global maxResults
        maxResults = event.GetString()
        
    def OnDownload(self, event):
        def UpdateGauge(total, recvd, ratio, rate, eta):
            self.progressGauge.SetValue((total/recvd)*100)
            
        global searchString
        global maxResults
        downloadFolder = file_reader.readFromFile("musicDirectory")
        songDownloader.init()
        stream = songDownloader.searchVideos(searchString, maxResults)
        stream.download(downloadFolder, quiet = True, callback = UpdateGauge)
        self.Destroy()
    
class openPlaylistDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(openPlaylistDialog, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info = wx.StaticText(self, label = "Input: ")
        hSizer.Add(self.info)
        
        self.textInput = wx.TextCtrl(self, size=(300, -1))
        self.Bind(wx.EVT_TEXT, self.OnChange, self.textInput)
        hSizer.Add(self.textInput, 1)

        self.g1 = wx.Gauge(self, -1, 100, (100, 100), (250, 25))
        self.g2 = wx.Gauge(self, -1, 100, (100, 100), (250, 25))

        self.directory = wx.StaticText(self, label = file_reader.readFromFile("musicDirectory"))

        self.downloadButton = wx.Button(self, label = "Open Playlist")
        self.Bind(wx.EVT_BUTTON, self.OnDownload, self.downloadButton)
        
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.g1, 0, wx.CENTER)
        mainSizer.Add(self.g2, 0, wx.CENTER)
        mainSizer.Add(self.directory, 0, wx.CENTER)
        mainSizer.Add(self.downloadButton, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

        self.SetSize((350, 150))
        self.SetTitle("Input playlist URL")

    def OnChange(self, event):
        global playlistString
        playlistString = event.GetString()
    def OnDownload(self, event):
        def UpdateGauge(total, recvd, ratio, rate, eta):
            self.g2.SetValue((total/recvd)*100)
        
        global playlistString
        downloadFolder = file_reader.readFromFile("musicDirectory")
        songDownloader.init()
        playlist = songDownloader.downloadPlaylist(playlistString)
        for i in range(0, len(playlist['items'])):
            self.g1.SetValue(((i+1.0)/len(playlist['items']))*100)
            wx.Yield()
            stream = playlist['items'][i]['pafy'].getbestaudio("m4a")
            wx.Yield()
            self.g2.SetValue(0)
            stream.download(downloadFolder, quiet = True, callback = UpdateGauge)
            wx.Yield()
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

try:
    os.remove("errorLog.txt")
except WindowsError:
    True = True
app = wx.App(redirect = 1, filename = "errorLog.txt")
frame = wx.Frame(None, wx.ID_ANY, "Youtube Song Downloader")
panel = MainPanel(frame)
frame.Show()
app.MainLoop()
