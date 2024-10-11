def showPopup(title, text):
    import os
    from pync import Notifier

    Notifier.notify(text, title=title, app_name="ciudadania")
    # Notifier.remove(os.getpid())
    # Notifier.list(os.getpid())