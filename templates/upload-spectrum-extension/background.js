// 调试日志
function debugLog(message) {
  console.log('[后台脚本]', message);
}

// 创建右键菜单
chrome.runtime.onInstalled.addListener(() => {
  debugLog("正在创建右键菜单...");
  chrome.contextMenus.create({
    id: "uploadApparatusFile",
    title: "_______上传谱图文件_______",
    contexts: ["page"]
  }, () => {
    if (chrome.runtime.lastError) {
      debugLog("创建菜单错误:", chrome.runtime.lastError);
    } else {
      debugLog("右键菜单创建成功");
    }
  });
});

// 处理右键菜单点击
chrome.contextMenus.onClicked.addListener((info, tab) => {
  debugLog("右键菜单被点击，菜单ID:", info.menuItemId);

  if (info.menuItemId === "uploadApparatusFile") {
    debugLog("准备打开文件选择器，标签ID:", tab.id);

    // 创建文件输入元素
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      func: () => {
        console.log('[内容脚本] 正在创建文件输入元素');
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '*';

        input.onchange = async (e) => {
          const file = e.target.files[0];
          console.log('[内容脚本] 文件已选择:', file ? file.name : '无文件');

          if (!file) return;

          // 读取文件为Base64
          const reader = new FileReader();
          reader.onload = () => {
            const base64Data = reader.result.split(',')[1];
            console.log('[内容脚本] 文件读取完成，大小:', base64Data.length);

            // 发送到后台脚本
            chrome.runtime.sendMessage({
              action: "fileSelected",
              fileData: {
                base64: base64Data,
                name: file.name
              }
            }, (response) => {
              if (chrome.runtime.lastError) {
                console.error('[内容脚本] 发送消息错误:', chrome.runtime.lastError);
              } else {
                console.log('[内容脚本] 消息发送成功');
              }
            });
          };

          reader.onerror = (error) => {
            console.error('[内容脚本] 文件读取错误:', error);
          };

          reader.readAsDataURL(file);
        };

        console.log('[内容脚本] 触发文件选择对话框');
        input.click();
      },
      args: []
    }).then(() => {
      debugLog("文件选择器脚本注入成功");
    }).catch(error => {
      debugLog("脚本注入失败:", error);
    });
  }
});

// 处理来自内容脚本的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  debugLog("收到消息:", message.action);

  if (message.action === "fileSelected") {
    debugLog("收到文件数据，准备转发到内容脚本");

    // 转发到内容脚本
    chrome.tabs.sendMessage(sender.tab.id, message, (response) => {
      if (chrome.runtime.lastError) {
        debugLog("转发消息错误:", chrome.runtime.lastError);
      } else {
        debugLog("消息转发成功");
      }
    });
  }

  return true; // 保持消息通道开放
});
