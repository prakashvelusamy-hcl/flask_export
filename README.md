kubectl label namespace default prometheus=kube-prometheus-stack


kubectl label service two-tier-app-service app=flask-app

kubectl patch service two-tier-app-service \
  -p '{"metadata": {"labels": {"app": "flask-app"}}}'

kubectl port-forward svc/kube-prometheus-stack-prometheus -n monitoring 9090 --address 0.0.0.0