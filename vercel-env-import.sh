#!/bin/bash
# Vercel环境变量批量导入脚本

# 检查是否安装了Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "错误: 未安装Vercel CLI"
    echo "请先安装: npm i -g vercel"
    exit 1
fi

# 检查是否已登录
if ! vercel whoami &> /dev/null; then
    echo "请先登录Vercel:"
    vercel login
fi

# 读取.env.vercel文件并导入环境变量
echo "开始导入环境变量..."

while IFS='=' read -r key value || [ -n "$key" ]; do
    # 跳过空行和注释
    if [[ -z "$key" ]] || [[ "$key" =~ ^[[:space:]]*# ]]; then
        continue
    fi
    
    # 去除前后空格
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    
    if [[ -n "$key" && -n "$value" ]]; then
        echo "导入: $key"
        echo "$value" | vercel env add "$key" production preview development
    fi
done < .env.vercel

echo "环境变量导入完成！"
echo "请在Vercel Dashboard中验证所有变量是否已正确添加"

