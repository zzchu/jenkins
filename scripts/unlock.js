
UIATarget.onAlert = function onAlert(alert){
    var title = alert.name();
    UIALogger.logWarning("Alert with title ’" + title + "’ encountered!");
    return false;
}

var target = UIATarget.localTarget();
UIATarget.unlock;
