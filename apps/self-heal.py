from kubernetes import client, config, watch
import time

config.load_kube_config()

v1 = client.CoreV1Api()

w = watch.Watch()

print("Watching for CrashLoopBackOff pods...")

for event in w.stream(v1.list_pod_for_all_namespaces):

    pod = event['object']

    if pod.status.container_statuses:

        for container in pod.status.container_statuses:

            waiting = container.state.waiting

            if waiting and waiting.reason == "CrashLoopBackOff":

                pod_name = pod.metadata.name
                namespace = pod.metadata.namespace

                print(f"[ALERT] CrashLoopBackOff detected: {pod_name}")

                try:

                    v1.delete_namespaced_pod(
                        name=pod_name,
                        namespace=namespace
                    )

                    print(f"[HEALED] Restarted pod: {pod_name}")

                except Exception as e:

                    print(f"Error healing pod: {e}")

    time.sleep(2)