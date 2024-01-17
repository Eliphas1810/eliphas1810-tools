var selectNewTabId = "SelectNewTab";

//マウスの右クリック メニューに追加
chrome.contextMenus.create({
    id: selectNewTabId,
    title: "リンクを新しいタブで開いて選択状態にする",
    contexts: ["link"]
});

//マウスの右クリック メニューで自作のメニューがクリックして選択された時の処理を追加
chrome.contextMenus.onClicked.addListener((info, tab) => {

    //マウスの右クリック メニューで自作のメニューがクリックして選択された場合
    if (info.menuItemId == selectNewTabId) {

        //リンクを新しいタブで開いて選択状態にします。
        chrome.tabs.create({url: info.linkUrl, selected: true});
    }
});
