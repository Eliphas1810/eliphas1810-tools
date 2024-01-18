//マウスの右クリック メニューに、この拡張機能が追加した自作のメニューが存在する場合は、それだけを削除
//
//これを起動しないと、Chromeを閉じてから再び開いた場合に、自作のメニューの追加の重複エラーが発生してしまいます。
//
//chrome.runtime.onInstalled.addListener(() => {});を利用すると、Chromeを閉じてから再び開いた場合に、この拡張機能が起動されないので、自作のメニューは存在するが、動作しなく成ってしまいます。
//
chrome.contextMenus.removeAll();

//マウスの右クリック メニューに、自作のメニューを追加
chrome.contextMenus.create({
    id: "SelectNewTab",
    title: "リンクを新しいタブで開いて選択状態にする",
    contexts: ["link"]
});

//マウスの右クリック メニューで、自作のメニューがクリックして選択された時の処理を追加
chrome.contextMenus.onClicked.addListener((info, tab) => {

    //マウスの右クリック メニューで、自作のメニューがクリックして選択された場合
    if (info.menuItemId == "SelectNewTab") {

        //リンクを新しいタブで開いて選択状態にします。
        chrome.tabs.create({url: info.linkUrl, selected: true});
    }
});
