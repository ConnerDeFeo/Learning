# Kubernetes: Zero to Deployed on AWS

A hands-on, incremental beginner course. **One new concept per module.** Each
module: read the theory beat, apply it to the running app, verify it works, then
move on. Do not stack concepts — if a module introduces two things, split it.

---

## Ground rules & conventions

- **Local first, cloud second.** Modules 0–18 run on a free local cluster
  (`kind`). Only Phase 5 touches AWS, where you pay real money.
- **The app grows with you.** You start with one container and end with a
  multi-tier app running on EKS behind an Ingress. You never rebuild from
  scratch — each module edits or adds to what exists.
- **Every module ends in a green checkmark.** A concrete `kubectl` command (or
  `curl`) proves the concept worked before you continue.
- **Suggested app:** FastAPI backend + Postgres + (optional) a static frontend.
  Swap in anything — the app is just a vehicle for the K8s concepts.
- **Repo layout suggestion:**
  ```
  /app            # source for the container(s)
  /manifests      # k8s YAML, one subfolder per phase
  /infra          # Terraform for EKS (Phase 5)
  /.github         # CI/CD workflow (Phase 6)
  ROADMAP.md      # this file — check modules off as you go
  ```
- **Version note:** kubectl, kind, EKS, and the AWS Load Balancer Controller
  move fast. Pin versions in your notes and cross-check anything
  version-specific against current official docs when you hit it.

---

## Phase 0 — Foundations & Setup

**M0 · Repo & tooling scaffolding**
- Concept: how this course works (theory → manifest → verify loop).
- Do: create the repo, install `docker`, `kubectl`, `kind`. Nothing else.
- Verify: `kubectl version --client` and `kind version` both print.

**M1 · What Kubernetes actually is (pure theory)**
- Concept: declarative desired-state + the control loop. You describe *what*
  you want; K8s continuously reconciles reality toward it.
- Do: no hands-on. Write a half-page in your own words: control plane vs nodes,
  "desired state," reconciliation.
- Verify: you can explain "declarative vs imperative" without notes.

**M2 · Containerize one app (Docker refresher)**
- Concept: an image is the unit K8s actually runs. K8s orchestrates
  containers; it does not build them.
- Do: write a Dockerfile for the backend, build it, run it with `docker run`.
- Verify: `curl localhost:PORT` hits your app in a container.

**M3 · A local cluster + kubectl**
- Concept: a cluster is nodes + a control plane; `kubectl` is how you talk to it.
- Do: `kind create cluster`. Learn `get nodes`, `get pods -A`, `cluster-info`.
- Verify: `kubectl get nodes` shows a Ready node.

---

## Phase 1 — Core Workload Objects

**M4 · Pods**
- Concept: the smallest deployable unit — one or more containers sharing a
  network/storage context. You rarely create these directly, but you must
  understand them.
- Do: run a pod imperatively, then rewrite it as a `pod.yaml` and `apply` it.
- Verify: `kubectl get pods` shows Running; `kubectl logs` shows app output.

**M5 · Labels & selectors**
- Concept: the glue. Labels tag objects; selectors query them. Almost every
  higher-level object finds its pods this way.
- Do: label your pod, then select it with `kubectl get pods -l key=value`.
- Verify: your selector returns exactly the pod you expect.

**M6 · ReplicaSets**
- Concept: keep N identical pods alive (self-healing). Motivates Deployments.
- Do: create a ReplicaSet, delete a pod, watch it get recreated.
- Verify: replica count self-heals back to desired after you `delete pod`.

**M7 · Deployments**
- Concept: the object you actually use day-to-day. Manages ReplicaSets for you
  and enables rolling updates (M16).
- Do: convert your ReplicaSet into a Deployment.
- Verify: `kubectl get deploy` shows all replicas available.

**M8 · Services (ClusterIP)**
- Concept: pods are ephemeral and get new IPs; a Service gives a stable address
  and load-balances across matching pods (via labels/selectors, M5).
- Do: add a ClusterIP Service in front of the backend Deployment.
- Verify: from a temp pod, `curl` the Service DNS name and reach the backend.

**M9 · Namespaces**
- Concept: logical partitions for organizing and isolating objects.
- Do: move the app into its own namespace.
- Verify: `kubectl get pods -n yourns` works; default namespace is empty of it.

---

## Phase 2 — Configuration & State

**M10 · ConfigMaps**
- Concept: externalize non-secret config out of the image.
- Do: move an app setting into a ConfigMap, inject it as an env var.
- Verify: change the ConfigMap value, restart, see the new value take effect.

**M11 · Secrets**
- Concept: same idea as ConfigMaps but for sensitive values (base64-encoded, not
  encrypted by default — note the caveat).
- Do: store the DB password as a Secret; inject into the backend.
- Verify: app reads the credential from the Secret, not from source.

**M12 · Volumes (the ephemeral-storage problem)**
- Concept: container filesystems die with the pod. `emptyDir` shows the problem
  and the volume-mount mechanics.
- Do: mount an `emptyDir`, write a file, delete the pod, observe data loss.
- Verify: you can articulate *why* you need durable storage next.

**M13 · PersistentVolumes & PVCs**
- Concept: durable storage decoupled from pod lifecycle. This is where Postgres
  enters as a stateful tier.
- Do: add a Postgres pod backed by a PVC; point the backend at it.
- Verify: write data, delete the Postgres pod, confirm data survives the restart.

> Stretch (optional): **StatefulSets** — stable identities/storage for
> replicated stateful apps. Skip for the core beginner path.

---

## Phase 3 — Reliability & Operations

**M14 · Health probes**
- Concept: liveness (restart if broken), readiness (hold traffic until ready),
  startup (grace period for slow boots).
- Do: add readiness + liveness probes to the backend.
- Verify: kill the health endpoint and watch K8s react correctly.

**M15 · Resource requests & limits**
- Concept: requests drive scheduling; limits cap usage. The basis for autoscaling.
- Do: set CPU/memory requests and limits on the backend.
- Verify: `kubectl describe pod` shows them; pod still schedules and runs.

**M16 · Rolling updates & rollbacks**
- Concept: Deployments replace pods gradually with zero downtime — and can undo.
- Do: ship a v2 image via rolling update, then `rollout undo` back to v1.
- Verify: watch the rollout; confirm no dropped requests; rollback restores v1.

**M17 · Autoscaling (HPA)** *(stretch but recommended)*
- Concept: scale replica count automatically off metrics (needs metrics-server).
- Do: add an HPA targeting CPU; generate load.
- Verify: replicas scale up under load, back down when it subsides.

---

## Phase 4 — Exposing the App

**M18 · Ingress + ingress controller**
- Concept: a single external entrypoint with host/path routing, instead of one
  Service-per-app exposure. Requires an ingress controller running in-cluster.
- Do: install an ingress controller (e.g. ingress-nginx), add Ingress rules
  routing `/api` to the backend (and `/` to the frontend if you built one).
- Verify: one hostname reaches multiple Services through path-based routing.

---

## Phase 5 — Go to AWS (EKS)

> **Cost warning.** From here you pay: EKS control plane (~$0.10/hr), worker
> nodes, and a load balancer. Tear everything down when not actively using it.
> Nothing new about Kubernetes is learned by leaving it running.

**M19 · EKS mental model (theory)**
- Concept: what a managed control plane gives you and what changes vs local —
  IAM everywhere, cloud load balancers, real networking, real cost.
- Do: no hands-on. Note the differences you expect to hit.
- Verify: you can list 3 things that differ from your `kind` cluster.

**M20 · Provision EKS with Terraform**
- Concept: infrastructure-as-code for the cluster (you already know Terraform).
- Do: stand up a minimal EKS cluster + a small managed node group.
- Verify: `aws eks update-kubeconfig` then `kubectl get nodes` shows AWS nodes.

**M21 · ECR — the image registry**
- Concept: EKS pulls images from a registry; local images aren't visible to it.
- Do: create an ECR repo, build/tag/push your backend image.
- Verify: the image appears in ECR and is pullable.

**M22 · Deploy the app to EKS**
- Concept: your manifests are portable — the same YAML runs on a real cluster.
- Do: apply your Deployment/Service/Config/Secret/PVC manifests to EKS
  (PVC now backed by an EBS-based StorageClass).
- Verify: `kubectl get pods` on EKS shows the app Running.

**M23 · Expose on AWS (LoadBalancer / ALB)**
- Concept: cloud-native exposure — a LoadBalancer Service or the AWS Load
  Balancer Controller provisioning a real ALB from your Ingress.
- Do: install the AWS Load Balancer Controller; expose the app via Ingress → ALB.
- Verify: hit the public ALB DNS name from your browser.

**M24 · IRSA — pod-level AWS permissions** *(stretch)*
- Concept: give a specific pod scoped AWS permissions via a service account,
  instead of node-wide credentials.
- Do: bind an IAM role to a service account used by one workload.
- Verify: the pod can call the intended AWS API and nothing broader.

**M25 · Teardown & cost audit**
- Concept: operational discipline — leaving clusters up is how bills happen.
- Do: `terraform destroy`, delete the ECR repo/images, confirm the ALB is gone.
- Verify: Cost Explorer / the console show no lingering EKS, EC2, or ELB charges.

---

## Phase 6 — Capstone & Next Steps

**M26 · CI/CD with GitHub Actions**
- Concept: automate build → push to ECR → deploy to EKS on every push to main.
- Do: write one workflow that builds the image, pushes to ECR, and applies
  manifests to the cluster.
- Verify: a commit to main lands a new version on EKS with no manual steps.

**M27 · Helm intro** *(stretch)*
- Concept: package and template your manifests instead of maintaining raw YAML.
- Do: convert your app into a small Helm chart with values.
- Verify: `helm install`/`upgrade` deploys and updates the app.

**M28 · Observability starter + where to go next**
- Concept: you can't operate what you can't see; know your next learning edges.
- Do: explore `kubectl logs`/`events`/`describe` as a debugging loop; note
  next topics (RBAC, network policies, GitOps/ArgoCD, service mesh).
- Verify: you can debug a broken pod using only cluster introspection.

---

### Core path vs stretch
**Core beginner path:** M0–M16, M18–M23, M25–M26.
**Stretch (do after the core clicks):** M17 (HPA), M24 (IRSA), M27 (Helm),
StatefulSets, plus the M28 "next topics."