# Cloud & Container Security Design (Section 16)

## 1. Architectural Cloud & Infrastructure Controls

This document details the cloud infrastructure and container security posture for deploying the **CyberOS Firewall Engine** in cloud-native containerized environments (AWS ECS / Kubernetes / Local Docker Lab).

| Cloud Security Domain | Technical Implementation Control | Enforcement Layer |
| :--- | :--- | :--- |
| **IAM & Least Privilege** | IAM roles assigned via service accounts (IRSA). Firewall container runs as non-root user (`uid 10001`). | Dockerfile / AWS IAM |
| **Network Segmentation** | Virtual Private Cloud (VPC) with private subnets for rule evaluation engines; API gateway restricted via Security Groups. | VPC / Security Groups |
| **Storage Security** | Policy files (`firewall_rules.json`) stored on encrypted EBS/EFS volumes with restricted POSIX file permissions (`600`). | OS Storage Layer |
| **Secrets Management** | AWS Secrets Manager / HashiCorp Vault injection into environment runtime (`.env` never committed to images). | Runtime Injector |
| **Encryption** | KMS customer-managed keys for data at rest (AES-256); TLS 1.3 for all management endpoints in transit. | AWS KMS / TLS |
| **Logging & Monitoring** | CloudWatch Logs integration with continuous ingestion of container STDOUT/STDERR streams. | CloudWatch Daemon |
| **Configuration Drift** | Infrastructure as Code (Terraform) enforced via CI/CD pipelines with automated drift detection (`terraform plan`). | CI/CD Pipeline |
| **Container Security** | Minimaldistroless/Alpine base images, multi-stage builds, dynamic vulnerability scanning with Trivy/Clair. | GitHub Actions / Trivy |
| **Backup & Disaster Recovery** | Automated snapshot policies for dynamic rulesets; Multi-AZ deployment for high-availability failover. | AWS Backup / Multi-AZ |

---

## 2. Container Security & Image Hardening Matrix

### Dockerfile Hardening Controls
* **Base Image:** Alpine Linux (`alpine:3.19`) to drastically minimize attack surface and dynamic binary footprint.
* **Privilege Reduction:** Standard execution drops `CAP_SYS_ADMIN` and only retains `CAP_NET_ADMIN` / `CAP_NET_RAW` for raw packet sniffing operations in `packet_sniffer.py`.
* **Read-Only Root Filesystem:** Container root filesystem is mounted as read-only (`--read-only`), with temporary write access restricted to isolated `/tmp` volumes.

---

## 3. Disaster Recovery & Infrastructure Resilience Plan

1. **Recovery Point Objective (RPO):** Maximum allowable data loss $\le 5\text{ minutes}$ via automated continuous S3 backup synchronization of policy states.
2. **Recovery Time Objective (RTO):** Maximum operational downtime $\le 2\text{ minutes}$ achieved via automated container re-instantiation across healthy availability zones.
