---
layout: post
title:  "Making IBM Cloud for Financial Services Work for You"
date: '2023-03-03T00:00:00.000-06:00'

description: "See how the unique industry-specific capabilities of IBM Cloud for Financial Services are designed to help you reduce risk and accelerate cloud adoption (including my part in building it)."
tags:
- ibm
- cloud
- financial services
- security
- compliance
- architecture
- nist
categories: [Architecture]
modified_time: '2023-03-03T00:00:00.000-06:00'

image:
  path: "/images/2023-03-03-making-ibm-cloud-for-financial-services-work-for-you/ibm_cloud_financial_services_social.png"
  show: false
---

# Introduction

You may recall that in my [previous post](/2021/08/evolving-the-ibm-cloud-console-with-microservices-a-nodejs-success-story.html), I mentioned that I had left the IBM Cloud console team to take on a new role as an architect for [IBM Cloud for Financial Services](https://www.ibm.com/cloud/financial-services). This post gives me a chance to share a bit more about what that work involves. I've been fortunate to be a key contributor and lead architect for many parts of the effort, and it's been a great follow-up chapter in my career.

Financial services is one of the most heavily regulated technology environments in the world. Banks, insurance companies, and financial institutions face an enormous burden when it comes to cloud adoption: they need to demonstrate regulatory readiness not just for themselves, but also for the third-party software and services they rely on. That's exactly the problem IBM Cloud for Financial Services is designed to solve.

In this post, I'll cover the key points from [a blog](https://www.ibm.com/new/product-blog/making-ibm-cloud-for-financial-services-work-for-you) I co-authored with colleague [Erick de Carty](https://www.linkedin.com/in/erickcarty/) on the IBM web site, which goes into each of these capabilities in more detail.

# IBM Cloud for Financial Services at a Glance

[IBM Cloud®](https://cloud.ibm.com) is well-suited for regulated workloads with its end-to-end security capabilities and support for a wide range of compliance programs. IBM Cloud for Financial Services extends that foundation with an industry-driven platform tailored specifically for financial services workloads. It hosts a rich ecosystem of IBM Cloud and partner services that makes it easier to both achieve and _demonstrate_ regulatory compliance.

The **IBM Cloud Framework for Financial Services** is the practical toolkit that makes all of this work. It provides four key accelerators:

- A comprehensive set of control requirements designed to address the security and regulatory compliance obligations of financial institutions
- Detailed implementation guidance for each control requirement, paired with concrete reference architectures
- Automation to deploy and configure those reference architectures with speed and consistency
- Tools to monitor compliance continuously, remediate issues, and generate evidence of compliance

# Industry-Specific Control Requirements

The framework's 565 control requirements are its foundation. They cover administrative, technical, and physical concerns that are common across the financial services industry. The requirements were initially based on NIST 800-53 and have been significantly enhanced through collaboration with major financial institutions around the world. As the regulatory landscape evolves, the framework is updated to reflect new industry standards and feedback from partners.

IBM Cloud services that have evidenced compliance to these requirements are designated as **IBM Cloud for Financial Services Validated**. This means you can use those components for your financial services workloads knowing that the control requirements have been integrated into the technology stack. There is also a growing partner ecosystem with the Financial Services Validated designation, which reduces the time and effort required to vet third-party risk and compliance.

# Guidance and Reference Architectures

The framework provides detailed implementation and evidence guidance for each control requirement. It's one thing to have a list of controls; it's another entirely to know _how_ to satisfy them in a real deployment. That's where the guidance and the three pre-defined reference architectures come in:

1. **IBM Cloud® Virtual Private Cloud (VPC)** — Establishes a private-cloud-like computing environment on shared public cloud infrastructure, with options for IBM Cloud Virtual Servers for VPC and/or Red Hat® OpenShift® on IBM Cloud® for compute.
2. **IBM Cloud® Satellite** — Builds a hybrid environment that brings the scalability and on-demand flexibility of public cloud services to applications and data running in your secure private cloud (for example, on-premises).
3. **IBM Cloud for VMware® Regulated Workloads** — An extension of the VMware vCenter Server® offering that delivers a secure, high-performance platform for workloads already rooted in VMware infrastructure.

Each of these architectures demonstrates how to stitch together Financial Services Validated ecosystem components as a secure basis for running your own financial services workloads on IBM Cloud. I made significant contributions to the implementation guidance accompanying the control requirements, and served as the lead architect and author for the VPC and Satellite architectures — with a focus on resilience, data integrity, security, and disaster recovery.

# Automated Deployable Architectures

The framework provides Infrastructure as Code (IaC) using Terraform to automate deployment of the VPC reference architecture. This lets you deploy a reference architecture with greater speed, less risk, and reduced cost compared to manual configuration.

The automation can be run as an [IBM Cloud project](https://cloud.ibm.com/docs/secure-enterprise?topic=secure-enterprise-understanding-projects) to support a secure software development lifecycle (SDLC). When using a project, **Code Risk Analyzer** is automatically added to your workflow, providing code and security scanning against a set of compliance checks mapped to a subset of the control requirements. If any checks fail, the Terraform is not executed. This is a concrete example of "shift left" DevSecOps, where security and vulnerability checks are pushed earlier into the development lifecycle rather than discovered at the end.

# Continuous Compliance Monitoring

Deploying a compliant architecture is only the start. Maintaining that compliance posture over time is where the real operational challenge lies, as configurations drift, new services are added, and the threat landscape changes.

With [IBM Cloud® Security and Compliance Center](https://cloud.ibm.com/security-compliance/overview), you can integrate daily, automatic compliance checks directly into your SDLC to catch possible security flaws and configuration drift before they become bigger problems. Unlike Code Risk Analyzer (which analyzes Terraform before deployment), Security and Compliance Center runs its tests against a live system.

Security and Compliance Center includes a pre-defined IBM Cloud for Financial Services profile with a set of automated tests appropriate for the VPC reference architecture, mapped to a growing subset of control requirements. A successful scan doesn't guarantee overall regulatory compliance, but it provides a meaningful, point-in-time statement of your posture against the controls for a specific group of resources.

For my part, I led a workgroup that combed through all 565 controls and their guidance to determine which could be validated through automated testing. We then defined the resulting set of tests that make up that SCC profile.

# Conclusion

A significant part of my current work is focused on making it possible for financial institutions and ISVs to build on the cloud knowing that the underlying platform and their own architectures can meet the rigorous demands of the financial services industry. The IBM Cloud Framework for Financial Services, with its control requirements, reference architectures, automated deployments, and continuous compliance monitoring, is the practical result of that work.

My hope is that these resources free up your team so that you can focus on delivering value to your clients rather than wrestling with compliance documentation. If you're ready to go deeper, [the full blog post](https://www.ibm.com/new/product-blog/making-ibm-cloud-for-financial-services-work-for-you) walks through each capability in detail.
