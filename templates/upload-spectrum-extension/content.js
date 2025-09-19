// 调试日志
function debugLog(message, data) {
    console.log('[iframe脚本]', message, data || '');
}

debugLog("脚本已加载，当前URL:", window.location.href);


// 存储提取的数据
let extractedData = {
    batch_code: null,
    equipment_code: null
};

// 提取数据函数
function extractData() {
    try {
        debugLog("正在提取数据...");

        // 提取 batch_code
        const batchInput = document.querySelector('input[name="txt_batch_code"]');
        extractedData.batch_code = batchInput ? batchInput.value : null;
        debugLog("提取到batch_code:", extractedData.batch_code);

        // 提取 equipment_code
        const equipmentInput = document.querySelector('input[name="txt_apparatus"]');
        if (equipmentInput && equipmentInput.value) {
            debugLog("原始设备值:", equipmentInput.value);
            const matches = equipmentInput.value.match(/\(([^)]+)\)/);
            if (matches && matches[1]) {
                extractedData.equipment_code = matches[1].replace(/-/g, '_');
                debugLog("处理后equipment_code:", extractedData.equipment_code);
            }
        }
    } catch (error) {
        debugLog("提取数据错误:", error);
    }
}

// 上传文件函数
async function uploadFile(fileData) {
    debugLog("开始上传流程，文件:", fileData.name);

    if (!extractedData.batch_code || !extractedData.equipment_code) {
        const errorMsg = "无法获取必要数据: " +
            `batch_code=${extractedData.batch_code}, ` +
            `equipment_code=${extractedData.equipment_code}`;
        debugLog(errorMsg);
        alert(errorMsg);
        return;
    }

    try {
        debugLog("构建SOAP请求...");

        // 构建SOAP请求XML
        const soapRequest = `<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <UploadApparatusFile xmlns="http://tempuri.org/">
              <token>etims@yunce</token>
              <buffer>${fileData.base64}</buffer>
              <create_company_id>10141</create_company_id>
              <batch_code>${extractedData.batch_code}</batch_code>
              <file_name>${fileData.name}</file_name>
              <equipment_code>${extractedData.equipment_code}</equipment_code>
              <file_parse_method>${extractedData.equipment_code}</file_parse_method>
            </UploadApparatusFile>
          </soap:Body>
        </soap:Envelope>`;

        debugLog("准备发送请求...");

        // 发送SOAP请求
        const response = await fetch(
            "http://10.1.31.200:8000/AppModules/ApparatusInterface/ApparatusInterfaceService.asmx",
            {
                method: "POST",
                headers: {
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": "http://tempuri.org/UploadApparatusFile"
                },
                body: soapRequest
            }
        );

        const responseText = await response.text();
        debugLog("上传响应:", {
            status: response.status,
            statusText: response.statusText,
            response: responseText
        });

        if (response.ok) {
            alert(`上传结果：
批次号: ${extractedData.batch_code}
设备代码: ${extractedData.equipment_code}
文件名: ${fileData.name}
状态: ${response.ok ? "成功" : "失败"}`);
        } else {
            alert(`文件上传失败: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        debugLog("上传过程中出错:", error);
        alert("上传错误: " + error.message);
    }
}


// 监听来自后台的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    debugLog("收到消息:", request.action);

    if (request.action === "fileSelected") {
        debugLog("收到文件数据");
        extractData(); // 确保数据是最新的
        uploadFile(request.fileData);
    }

    return true;
});

// 初始提取数据
extractData();
debugLog("内容脚本初始化完成");
