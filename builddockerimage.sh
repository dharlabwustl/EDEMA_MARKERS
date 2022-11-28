# ./bashtowriteDockerfile.sh
cat ./Dockerfile_part1 > Dockerfile
echo "  "
command=""
for x in *.json ;
do 
	command="${command}   ${x}  "
done
echo $command
python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/FROM_DOCUMENTS/docker-images/command2label.py  $command  >> ./Dockerfile
# imagename=$1
imagename=fsl502py369withpacksnltx
docker build -t sharmaatul11/${imagename} . 
docker push sharmaatul11/${imagename}  
