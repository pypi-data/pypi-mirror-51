## GVC基因组突变探测套件使用说明

GVC（Genomic Variant Caller）基因组突变探测套件是由志诺维思自主研发的一款人工智能变异探测加速软件。利用二代测序数据可以对遗传性胚系（Germline）和肿瘤体细胞（Somatic）变异进行检测分析，支持FASTQ或者BAM的标准文件输入格式，可对多种变异类型（SNP、SNV、sINDEL、SV和CNV）一次性同时探测，软件精准度超过主流公认的算法软件，突变探测的速度和运行效率平均提升20倍，包含比对的整体流程效率提升5倍。目前版本支持WGS、WES和Panel的测序类型，肿瘤变异探测必须为含对照的组织样品测序，肿瘤样品的覆盖深度建议在100X-1000X之间。客户如有对生产数据的模型定制、精度提升或其他测序应用场景的需求请直接联系我们的技术支持人员。

## 一、部署环境要求

```
Linux系统内核版本高于3.10
服务器内存大于16G
服务器线程数大于10
```

## 二、安装说明

### 1. 安装必须软件包

```
yum install -y epel-release
yum -y install docker python python-devel python-pip gcc zlib-devel bzip2-devel xz-devel 
systemctl start docker

```

*注意：用户必须可以运行docker命令才能运行GVC，如果需要让某个普通用户（例如 USER_NAME）具有此权限，可以使用如下命令. 参考：https://docs.docker.com/install/linux/linux-postinstall/*

```
groupadd docker
gpasswd -a USER_NAME docker
systemctl restart docker
#if you are currently login as USER_NAME
#please logout and login again
```

### 2. 获取GVC所需Docker镜像

*注意：如果本地下载docker hub里的镜像过慢，可以考虑在/etc/docker/daemon.json里增加如下配置来加速*

```
"registry-mirrors": 
	["https://registry.docker-cn.com",
	"http://hub-mirror.c.163.com",
	"https://docker.mirrors.ustc.edu.cn"]
```

最终的/etc/docker/daemon.json内容可以是这样：

```
{
  "live-restore": true,
  "registry-mirrors": 
  	["https://registry.docker-cn.com",
  	"http://hub-mirror.c.163.com",
  	"https://docker.mirrors.ustc.edu.cn"]
}
```

需要重启docker服务来让新配置生效

```
sudo systemctl restart docker
```

### 3.安装python相关组件

#### 安装python，以及独立python环境

```
#Please note, gvc4fastq can only run with Python 2.7
#Consider of using virtualenv to create a sperate env

##如果想启用一个名为venv的独立python运行环境，
##避免与当前python环境互相干扰，可以安装virtualenv
#pip install virtualenv
#virtualenv ~/venv       
#source ~/venv/bin/activate   #进入该独立的python环境

pip install gvc4fastq

```

### 4.获取模型文件包和docker包

GVC使用机器学习算法，使用GVC必须配合使用相应的模型文件。最新版本模型文件可以这样获取:

```
wget https://gvc.obs.cn-north-1.myhuaweicloud.com/gvc_lib.tar.gz
tar zxf gvc_lib.tar.gz
```

更新库文件中docker包版本信息并获取最新docker包

```
wget https://gvc.obs.cn-north-1.myhuaweicloud.com/version.json -O gvc_lib/version.json
cat gvc_lib/version.json |awk '{print $2}'|awk -F '"' '{print $2}'|xargs -I % docker pull %
```

### 5.安装license

#### 自动获取试用license

请登录 https://gvc.0cancer.cn/application 填写表单，按照邮件指引操作。

#### 正式采购

首先获取机器码

操作系统装好Docker后，可直接运行如下命令来获取机器码

```
docker run --network=host genowisgvc/id:latest
```

例如：

```
$ docker run --network=host genowisgvc/id:latest
IVDA-BBAA-LHep-zQAA:uU9c0qCsUnYKLNnEgagvKw==
```

联系志诺维思取得license文件

取得所有需要安装GVC的服务器的机器码，发送给我们客户支持信箱 support@genowis.com，我们将会给你们发送一个license.txt文件和gvc.lic文件，将这两个文件放入gvc_lib目录下即可完成激活。


## 三、使用说明

### 使用bam_vcf流程

```
bam_vcf.py:

usage: bam_vcf.py [options] input_json reference outpath

必要参数
    
    input_json:# json文件中配置了Normal BAM 和 Tumor BAM 的路径信息
               # 请使用bwa-mem比对生成的排序后的bam，暂不支持其他比对软件。
               # 肿瘤体细胞变异，json文件格式: 
               # {"N": ["/path/N.sort.bam"], "T": ["/path/T.sort.bam"]}
               # 遗传性胚系变异，json文件格式
               # {"T": ["/path/sample.sort.bam"] }

	           	            	
    reference: 
             # 参考序列，例如 /disk/human.fa
              # 注意此路径需要包含参考序列索引文件 /disk/human.fa.fai
               
    outpath：
             # 输出路径参数，例如 /disk/output
    
    --gvc_lib: 
             # 库文件和配置文件路径
    
    --strategy: 
             # 测序类型选择，支持WGS, WES和Panel
    
    --dbsnp:   
             # dbSNP库（The Single Nucleotide Polymorphism Database）
             # 包含三列，分别是 Chr, Position, rsID ，列之间通过tab隔开
	            
    --bed:     
             # bed文件包含三列，分别是chr, start, end, 通过tab隔
	
    --sample_name:   
             # 样品名
    --mutantType :   
             # somatic（肿瘤体细胞变异） ， germline （遗传性胚系变异） 可同时选择两者
	
可选参数：	
    --segmentSize:  
              # 默认单线程运行，此参数切分bam加速，
	      # 如20000000 ，对bed区域进行20M大小切分
    --maxCores: 
              #指定使用的最大线程数
    --maxMemory：
              #指定使用的最大内存数
    --CNV：
              #输出CNV结果
    --SV：
              #输出SV结果
```

### 示例：

```
$ bam_vcf.py \
	/absolute/path/to/demo/demo.json \    # input_json
	/absolute/path/to/demo/human.fa \     # gvc_lib path
	/absolute/path/to/demo/test \         # output path
	--dbsnp /absolute/path/to/demo/dbsnp_138-1000G-snp \
	--bed /absolute/path/to/demo/demo.bed \
	--gvc_lib /absolute/path/to/gvc_lib \ 
	--strategy WES  \
	--segmentSize 20000000 \
	--sample_name demo_sample_name \
	--mutantType  somatic 
	
	
```

### 使用fastq_vcf流程

```
fastq_vcf.py:

usage: fastq_vcf.py [options] input_json reference outpath

必要参数

    input_json:# json文件中配置了Normal BAM 和 Tumor BAM 的路径信息
              # 请使用bwa-mem比对生成的排序后的bam，暂不支持其他比对软件。
              # 肿瘤体细胞变异，json文件格式：
              # {
              #	"N": { "R1": ["/disk/N_1.fastq.gz"], "R2": ["/disk/N_2.fastq.gz"] },
              #	"T": { "R1": ["/disk/T_1.fastq.gz"], "R2": ["/disk/T_2.fastq.gz"] }
              # }
              # 遗传性胚系变异探测，json文件格式：
              # {
              #   "T": {"R1":["/disk/demo_1.fastq.gz"],"R2":["/disk/demo_2.fastq.gz"]}
              # }


  reference: 
              # 参考序列，例如 /disk/human.fa
              # 注意此路径需要包含参考序列索引文件 /disk/human.fa.fai

    outpath： 
              # 输出路径参数，例如 /disk/output

    --gvc_lib: 
             # 库文件和配置文件路径

    --strategy: 
              # 测序类型选择，支持WGS, WES和Panel

    --dbsnp: 
              # dbSNP库（The Single Nucleotide Polymorphism Database）
              # 包含三列，分别是 Chr, Position, rsID ，列之间通过tab隔开

    --bed:     
              # bed文件包含三列，分别是chr, start, end, 通过tab隔

    --sample_name:  
              # 样品名
    --mutantType :   
              # somatic（肿瘤体细胞变异） ， germline （遗传性胚系变异）可同时选择两者

可选参数：
    --segmentSize:  
              # 默认单线程运行，此参数切分bam加速，
              # 如20000000 ，对bed区域进行20M大小切分
    --maxCores: 
              #指定使用的最大线程数
    --maxMemory：
              #指定使用的最大内存数
    --CNV：
              #输出CNV结果
    --SV：
              #输出SV结果
```

### 示例：

```
$ fastq_vcf.py \
	/absolute/path/to/demo/demo.json \    # input_json
	/absolute/path/to/demo/human.fa \     # gvc_lib path
	/absolute/path/to/demo/test \         # output path
	--dbsnp /absolute/path/to/demo/dbsnp_138-1000G-snp \
	--bed /absolute/path/to/demo/demo.bed \
	--gvc_lib /absolute/path/to/gvc_lib \
	--strategy WES  \
	--segmentSize 20000000 \
	--sample_name demo_sample_name \
    --mutantType  somatic
```

## 四、测试实例

用户可以下载并执行一个小测试集来验证安装是否成功

```
#get reference data
wget --no-check-certificate https://gvc.obs.cn-north-1.myhuaweicloud.com/ref.tar.gz
tar zxf ref.tar.gz

#get test data set
wget --no-check-certificate https://gvc.obs.cn-north-1.myhuaweicloud.com/test_set.tar.gz
tar zxf test_set.tar.gz

#run GVC

#prepare the output folder
mkdir /tmp/output

#please use absolute path for all parameters
# we need these information to run GVC:
# path for fastq files
# path to reference
# output folder
# dbSNP file
# bed file
# gvc_lib pathname
# sample name
# WGS, WES or Panel
# Somatic or Germline
# You can read the user guide for more options

fastq_vcf.py  \
  $PWD/test_set/input.json \
  $PWD/ref/human.fa \
  /tmp/output    \
  --dbsnp $PWD/gvc_lib/dbsnp_138-1000G-snp \
  --bed $PWD/test_set/test.bed \
  --gvc_lib $PWD/gvc_lib  \
  --sample_name sample_name1 \
  --strategy Panel  \
  --mutantType Somatic \
  --mutantType Germline 

#you should see output like this after success:
Runtime:132.311218977(s)
BWA: Jobs=2.0 ,Threads=16 ,Total_time=18.2844610214(s)
Duplicate: Jobs=2.0 ,Threads=32 ,Total_time: 2.0171880722(s)
GVC: Jobs=1.0 ,Threads=1 ,Total_time: 27.1398601532(s)
QC: Jobs=1.0 ,Threads=5 ,Total_time: 18.7981309891(s)
```

#### *使用或安装过程中，遇到任何问题都可以随时联系我们*

*电话：010-58433158*

*邮箱：support@genowis.com*

志诺维思（北京）基因科技有限公司
