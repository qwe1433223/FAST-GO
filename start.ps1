Set-ExecutionPolicy RemoteSigned

# 获取命令行参数列表
$argsList = $args

# 检查是否传入了项目路径参数
if ($argsList.Length -eq 0) {
    Write-Host "usage：start.ps1 项目名称 是否继续上一次任务"
    Write-Host "       start.ps1 丁香园 0"
    Write-Host "usage：start.ps1 -P 丁香园 -C 1" 
    Exit
}

#路径
$资产收集 = Split-Path -Parent $MyInvocation.MyCommand.Definition
$fofaScriptPath = "$资产收集\\FOFA处理\处理.py"
$SurvivalScan = "$资产收集\\Web-SurvivalScan\\Web-SurvivalScan.py"
$URLS_TO_IPS = "$资产收集\\URLS_TO_IPS\\URLS_TO_IPS.py"
$bypassScriptPath = "$资产收集\\403_ByPasser\\403bypasser.py"
$OneForAll = "$资产收集\\01-子域名OneForAll\\oneforall.py"
$资产去重 = "$资产收集\\资产去重\\去重.py"

#参数
$project = $argsList[0]
if($argsList[1] -eq $null){
    $IS_CONTINUE = 0
}else{
    $IS_CONTINUE = $argsList[1]
}


function segmentation(){
    param (
        [string]$information
    )
    Write-Host ("-"*111) -ForegroundColor Red
    Write-Host ("-"*111) -ForegroundColor Red
    Write-Host ("-"*50)$information("-"*50) -ForegroundColor Red
    Write-Host ("-"*111) -ForegroundColor Red
    Write-Host ("-"*111) -ForegroundColor Red
}


$multilineStr = @"
usage：start.ps1 项目名称 是否继续上一次任务
       start.ps1 丁香园 0

1、将 $project\$project.txt 里的URL转换为 IP

2、使用FOFA处理脚本，从 FOFA处理\$project 这个目录下的所有.csv文件里获取URL
    输出到 ：
        $project\$project.txt
        E:\WORK\SRC\项目\$project\target\urls.txt

3、使用资产收集脚本扫描 $project\$project.txt 中的URL
    输出到 Web-SurvivalScan\$project\  目录下
    
"@

#创建文件夹
$folderPath = $资产收集 + "\\" + $project + "\\OneForAll"
if (-Not (Test-Path $folderPath)) {
    New-Item -Path $folderPath -ItemType Directory
}


# 执行 子域名爆破
segmentation("子域名爆破")
python $OneForAll "--targets" "$资产收集\\$project\\OneForAll目标界定.txt" "--path" "$资产收集\\$project\\OneForAll" "run"


# 执行 FOFA 处理脚本
segmentation("FOFA处理")
python $fofaScriptPath $project


# 执行 Web 存活扫描
segmentation("存活扫描")
$资产收集目标文件 = "$project\$project.txt"
python $SurvivalScan $资产收集目标文件


#URL转IP
segmentation("domain转IP")
python $URLS_TO_IPS $project


#资产去重
segmentation("模板资产去重")
python $资产去重 "-p" $project "-c" $IS_CONTINUE



#复制结果
#$content = Get-Content "$project/单独开发资产.txt"
#$path = "E:/WORK/SRC/项目/$project/target/urls.txt"
#$content | Set-Content -Path $path

#是否进行403资产绕过探测
segmentation("403 ByPass")
Write-Host "将对多个目标进行403 ByPass，不建议进行"
$userInput = Read-Host "是否进行403资产绕过探测? (y/n)"
if ($userInput -eq "y") {
    $path = $资产收集+"\\"+$project+"\\403.txt"
    $arguments = @($bypassScriptPath, "-U", $path, "-d", "//")
    Start-Process python -ArgumentList $arguments -NoNewWindow -Wait
} else {
    # 不进行绕过探测
}
