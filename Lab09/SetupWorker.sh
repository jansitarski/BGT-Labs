sudo apt-get -y install python3-pip
sudo pip install ray google-cloud-datastore Faker
until ray start --address='192.168.0.10:6379'
do
  echo "Try again"
done

