import os
import wx
import wx.lib.agw.multidirdialog as MDD
import processCSV 
wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"
class MyForm(wx.Frame):


 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Give India Backend Developer Challenge")
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        self.svPath = ""
        self.baseCurrency = "INR"
        self.isDone = False
        # create the buttons and bindings
        openFileDlgBtn = wx.Button(panel, label="Select the CSV", pos = (125,120))
        languages = ['INR', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'GBP', 'RON', 'SEK', 'IDR',
         'CAD', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'EUR', 'MYR', 'BGN', 'TRY', 'CNY', 'NOK',
         'NZD', 'ZAR', 'USD', 'MXN', 'SGD', 'AUD', 'ILS', 'KRW', 'PLN'] 
        label = wx.StaticText(panel, label = "Select the Base currency", pos = (100,50))
        self.choice = wx.Choice(panel,choices = languages,  pos = (125,75))
        self.btn = wx.Button(panel, label = "Process CSV", pos = (125,150))
        self.btn.Bind(wx.EVT_BUTTON,self.OnClicked)
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        if(self.isDone):
          newLable = wx.StaticText(panel, label = "Find the results.csv and notValid.csv in the same directory as main.py", pos = (60,175))

    def OnChoice(self,event): 
      self.baseCurrency = self.choice.GetString( self.choice.GetSelection() )
    def OnClicked(self,event): 
      processCSV.processCSV(self.svPath, self.baseCurrency)
      self.isDone = True
    def onOpenFile(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                self.svPath = path
                print(path)
        dlg.Destroy()
        
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()