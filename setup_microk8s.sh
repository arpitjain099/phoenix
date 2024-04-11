echo "Setting up cluster"
microk8s enable ingress
microk8s enable dns
microk8s enable registry
microk8s enable hostpath-storage
microk8s config > ~/.kube/microk8s-config
export KUBECONFIG=~/.kube/config:~/.kube/microk8s-config
kubectl config use-context microk8s

echo "#######################################################"
echo "You need to add the following line to your /etc/hosts file"
echo "    127.0.0.1       superset.phoenix.local"
echo "    127.0.0.1       oauth.phoenix.local"
echo "    127.0.0.1       api.phoenix.local"
echo ""
echo "#######################################################"
