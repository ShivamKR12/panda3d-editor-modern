import os

import wx


def file_dialog(message, wildcard, style, defaultDir=os.getcwd(), defaultFile=''):
    """
    Generic file dialog method. If False is returned then the user has hit
    cancel or not selected a valid path.
    """
    result = []
    dlg = wx.FileDialog(wx.GetApp().GetTopWindow(), message, defaultDir, defaultFile, wildcard, style)
    if dlg.ShowModal() == wx.ID_OK:
        if style & wx.FD_MULTIPLE:
            result = dlg.GetPaths()
        else:
            result = [dlg.GetPath()]
    dlg.Destroy()
    return result
    

def file_open_dialog(message, wildcard, style=0, defaultDir=os.getcwd(), defaultFile=''):
    """Generic file open dialog."""
    style = style | wx.FD_OPEN | wx.FD_CHANGE_DIR
    file_paths = file_dialog(message, wildcard, style, defaultDir, defaultFile)
    if style & wx.FD_MULTIPLE:
        return file_paths
    return next(iter(file_paths), None)


def file_save_dialog(message, wildcard, style=0, defaultDir=os.getcwd(), defaultFile=''):
    """Generic file save dialog."""
    style = style | wx.FD_SAVE | wx.FD_CHANGE_DIR
    file_paths = file_dialog(message, wildcard, style, defaultDir, defaultFile)
    return next(iter(file_paths), None)
    

def director_dialog(message, defaultPath=os.getcwd(), style=wx.DD_DEFAULT_STYLE):
    """Generic directory dialog."""
    dlg = wx.DirDialog(wx.GetApp().GetTopWindow(), message, defaultPath, style)
    if dlg.ShowModal() == wx.ID_OK:
        result = dlg.GetPath()
    else:
        result = False
    dlg.Destroy()
    
    return result
    

def message_dialog(message, caption, style):
    """Generic message dialog method."""
    dlg = wx.MessageDialog(wx.GetApp().GetTopWindow(), message, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    
    return result
    

def InformationDialog(message, caption='Information'):
    """Generic information dialog with ok button."""
    return message_dialog(message, caption, wx.ICON_INFORMATION | wx.OK)
    

def WarningDialog(message, caption='Warning'):
    """Generic warning dialog with ok button."""
    return message_dialog(message, caption, wx.ICON_WARNING | wx.OK)
    

def ErrorDialog(message, caption='Error'):
    """Generic error dialog with ok button."""
    return message_dialog(message, caption, wx.ICON_ERROR | wx.OK)
    

def YesNoDialog(message, caption, style=wx.ICON_QUESTION):
    """Generic message dialog with yes / no buttons."""
    return message_dialog(message, caption, style | wx.YES_NO)
    

def YesNoCancelDialog(message, caption, style=wx.ICON_QUESTION):
    """Generic message dialog with yes / no / cancel buttons."""
    return message_dialog(message, caption, style | wx.YES_NO | wx.CANCEL)
    

def ImgToBmp(filePath, size):
    """Return a wx bitmap from a filepath, scaled to the toolbar size."""
    # If path is not absolute, resolve it relative to project root
    if not os.path.isabs(filePath):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filePath = os.path.normpath(os.path.join(base_path, filePath))
    if not os.path.exists(filePath):
        print(f"[ERROR] Icon file does not exist: {filePath}")
        return wx.NullBitmap
    img = wx.Image(filePath)
    if not img.IsOk():
        print(f"[ERROR] Failed to load image: {filePath}")
        return wx.NullBitmap
    img.Rescale(size[0], size[1])
    bmp = wx.Bitmap(img)
    return bmp
    
    
def IdBind(self, event, id, handler, *args, **kwargs):
    self.Bind(event, lambda event: handler(event, *args, **kwargs), id=id)


def get_clicked_item(ctrl, evt):
    """Return the id for the item involved in the mouse event."""
    return ctrl.HitTest(wx.Point(evt.GetX(), evt.GetY()))[0]
