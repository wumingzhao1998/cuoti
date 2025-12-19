# Vercel部署问题修复

## 问题

部署失败，错误信息：
```
Error: A Serverless Function has exceeded the unzipped maximum size of 250 MB.
```

## 原因

`opencv-python` 和 `numpy` 包非常大（合计约200-300MB），导致Serverless Function超过Vercel的250MB限制。

## 解决方案

### 方案1：使用轻量版依赖（已实施）

已创建 `requirements-vercel.txt`，移除了 `opencv-python` 和 `numpy`：

- ✅ 代码已修改为可选依赖，自动降级到Pillow处理
- ✅ 图像处理功能仍然可用，但效果可能略差
- ✅ 部署包大小大幅减小

**当前 `requirements.txt` 已替换为轻量版**

### 方案2：使用外部图像处理服务（推荐用于生产环境）

对于生产环境，建议使用外部图像处理API：

1. **阿里云图像处理服务**
2. **腾讯云图像处理服务**
3. **AWS Rekognition**
4. **Google Cloud Vision API**

### 方案3：分离图像处理服务

将图像处理功能部署到单独的服务器或服务：
- 使用Docker部署到其他平台（如Railway、Render等）
- 或使用专门的图像处理API服务

## 当前状态

✅ **已完成的修改：**

1. 创建了 `requirements-vercel.txt`（轻量版）
2. 创建了 `requirements-full.txt`（完整版，本地开发用）
3. 修改了 `src/handwriting/remover.py`，支持可选opencv
4. 修改了 `src/ocr/processor.py`，支持可选opencv
5. 更新了 `vercel.json` 配置
6. 当前 `requirements.txt` 已使用轻量版

## 部署步骤

1. **确认当前使用的是轻量版依赖**：
   ```bash
   # requirements.txt 应该不包含 opencv-python 和 numpy
   ```

2. **重新部署到Vercel**：
   - 推送代码到GitHub
   - Vercel会自动重新部署
   - 或手动在Vercel Dashboard点击Redeploy

3. **验证部署**：
   - 检查部署日志，确认没有大小限制错误
   - 测试基本功能是否正常

## 功能影响

### 仍然可用的功能

- ✅ OCR识别（使用豆包API，不依赖opencv）
- ✅ 飞书集成
- ✅ AI引导和问题生成
- ✅ 基础图像处理（使用Pillow）

### 功能降级

- ⚠️ 去手写功能：使用Pillow基础处理，效果可能不如OpenCV
- ⚠️ 图像预处理：使用Pillow，功能有限

### 建议

如果去手写功能对效果要求高，建议：
1. 使用外部图像处理API
2. 或部署单独的图像处理服务
3. 或使用Vercel Pro（有更大的函数大小限制）

## 本地开发

本地开发时，可以使用完整版依赖：

```bash
pip install -r requirements-full.txt
```

这样可以在本地使用完整的OpenCV功能进行开发和测试。

## 回滚方案

如果需要恢复完整功能，可以：

1. 将 `requirements-full.txt` 复制为 `requirements.txt`
2. 但需要注意Vercel的250MB限制
3. 或考虑升级到Vercel Pro

