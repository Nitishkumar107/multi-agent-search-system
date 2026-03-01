#!/bin/bash
# Builds the custom Jenkins+Docker image entirely from WSL native filesystem

BUILD_DIR="$HOME/custom_jenkins_build"
mkdir -p "$BUILD_DIR"

echo "Writing Dockerfile to WSL native filesystem at $BUILD_DIR..."

cat > "$BUILD_DIR/Dockerfile" << 'EOF'
# Use the Jenkins Docker image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install Docker inside Jenkins container (Debian trixie compatible)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        lsb-release && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
        https://download.docker.com/linux/debian \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to Jenkins user
USER jenkins

# Set the entrypoint to run Jenkins
ENTRYPOINT ["/usr/local/bin/jenkins.sh"]
EOF

echo "Dockerfile written ($(wc -c < "$BUILD_DIR/Dockerfile") bytes)"
echo "Building jenkins-dind image..."

docker build -t jenkins-dind "$BUILD_DIR"

echo "Done!"
