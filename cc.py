# Exercise 5 – Virtual Instances, Load Balancing, Server Consolidation and Fault Tolerance
# Part 1: Create VMs and install Apache
# - Open VMware Workstation → select your Ubuntu VM → Manage → Clone → Create a full clone.
# - Power on the cloned VMs and open a terminal in each VM.
# - Run these commands on every VM, one after another:
# 1. Update packages: sudo apt update
# 2. Install Apache: sudo apt install apache2 -y
# 3. Enable Apache at startup: sudo systemctl enable apache2
# 4. Check Apache status: sudo systemctl status apache2
# 5. Edit the web page to give each VM a unique response: sudo nano /var/www/html/index.html
#    - Save using Ctrl + O, press Enter, then exit with Ctrl + X.
#    - Example: VM1 displays Hello from VM1, VM2 displays Hello from VM2.
# 6. Find the VM's IP address: ifconfig
# Part 2: Configure HAProxy load balancing
# - Choose one VM as the load balancer, separate from the backend VMs if possible.
# - Install HAProxy:
# 1. sudo apt update
# 2. sudo apt install haproxy -y
# 3. Open its configuration: sudo nano /etc/haproxy/haproxy.cfg
# 4. Add this configuration at the end of the file. Replace the IP placeholders with the actual backend VM IP addresses.

# frontend http_front
#     bind *:80
#     default_backend http_back

# backend http_back
#     balance roundrobin
#     server vm1 VM1_IP:80 check
#     server vm2 VM2_IP:80 check
#     server vm3 VM3_IP:80 check



# - Save and exit (Ctrl + O → Enter → Ctrl + X).
# - Restart, enable and verify HAProxy, in order:
# 1. sudo systemctl restart haproxy
# 2. sudo systemctl enable haproxy
# 3. sudo systemctl status haproxy
# 4. Open http://LOAD_BALANCER_IP in a browser.
# Expected result: the browser displays a backend VM's page. Refresh several times to check the round-robin distribution.
# Part 3: Server consolidation
# This part is mainly done through VMware settings and the Ubuntu terminal.
# - Open VMware Workstation and identify VMs with low usage or redundant workloads.
# - Select a VM with sufficient CPU, RAM and storage to host the combined workloads.
# - Open VM → Edit virtual machine settings → adjust Memory and Processors as required.
# - Copy the files/services from the VMs being consolidated to the target VM.
# - Start the services on the target VM and verify that they work.
# - After confirming everything works, power off the old VMs. Remove unused VMs through VMware → right-click VM → Remove.
# - Check CPU and memory utilization on the consolidated Ubuntu VM:
# 1. top
# 2. htop (optional; install with sudo apt install htop -y if needed)
# Part 4: Fault tolerance
# - In VMware Workstation, select the primary VM → VM → Manage → Clone → Create a full clone. This creates a backup VM.
# - To synchronize files between the primary and backup VMs:
# 1. sudo apt install rsync -y
# 2. rsync -av /source_directory/ user@BACKUP_VM_IP:/destination_directory
#   Replace the directories, username and IP address with your actual values. SSH access must be configured between the VMs.
# - To create a recovery point, select the critical VM → VM → Snapshot → Take Snapshot.
# - Name the snapshot, for example, Pre-Consolidation Snapshot.
# Expected result: multiple VMs run web services, HAProxy distributes requests, resources are consolidated, and a backup/snapshot is available for recovery.

# Exercise 6 – Task Scheduling and Load Balancing
# Part 1: Task scheduling using cron
# - Open VMware Workstation and power on the Ubuntu VM.
# - Open the terminal and create the script:
# 1. nano script.sh
# 2. Enter the following line in the file:
# echo "Hello Selcia"
# 3. Save using Ctrl + O → Enter → Ctrl + X.
# 4. Make the script executable:
# chmod +x script.sh
# - Open the cron editor:
# crontab -e
# - Add this line at the end to run the script every minute and append the output to a log:
# * * * * * /bin/bash /home/YOUR_USERNAME/script.sh >> /home/YOUR_USERNAME/output.log 2>&1
# Replace YOUR_USERNAME with your Ubuntu username. Using absolute paths ensures cron can locate the script and log file.
# - Save and exit the editor.
# - Wait one or two minutes, then verify the output:
# 1. cat output.log
# 2. tail -f /var/log/syslog | grep CRON
# Press Ctrl + C to stop watching the log.
# Expected result: Hello Selcia appears repeatedly in output.log, once per minute.
# Part 2: Configure load balancing
# - Choose one Ubuntu VM as the HAProxy load balancer and ensure the backend VMs are running Apache, as in Exercise 5.
# - Install HAProxy:
# 1. sudo apt update
# 2. sudo apt install haproxy -y
# 3. sudo nano /etc/haproxy/haproxy.cfg
# - Add the following configuration, replacing the IP placeholders with the backend VMs' actual IP addresses.

# frontend http_front
#     bind *:80
#     default_backend http_back

# backend http_back
#     balance roundrobin
#     server vm1 VM1_IP:80 check
#     server vm2 VM2_IP:80 check
#     server vm3 VM3_IP:80 check



# - Save and exit, then execute:
# 1. sudo systemctl restart haproxy
# 2. sudo systemctl enable haproxy
# 3. sudo systemctl status haproxy
# - Open http://LOAD_BALANCER_IP in your browser and refresh to observe different backend pages.
# Part 3: Advanced scheduling (optional)
# - Create the first script:
# nano script1.sh
#   Add a CPU-intensive task, for example:
# for i in {1..100000}; do echo "$i" > /dev/null; done
# - Create the second script:
# nano script2.sh
#   Add:
# date >> /home/YOUR_USERNAME/system_info.log
# - Save both scripts and make them executable:
# chmod +x script1.sh script2.sh
# - Open the cron editor:
# crontab -e
# - Add these lines to schedule both scripts every minute with different priorities:
# * * * * * nice -n 10 /bin/bash /home/YOUR_USERNAME/script1.sh
# * * * * * nice -n 0 /bin/bash /home/YOUR_USERNAME/script2.sh
# - Save and exit. Verify the second script's output using:
# cat /home/YOUR_USERNAME/system_info.log
# Expected result: cron executes tasks automatically, and nice assigns different CPU scheduling priorities. A higher nice value means lower priority.

# Exercise 7 – Hypervisor Clustering in a Cloud Environment
# This exercise is different from Exercises 5 and 6. Most steps use the VMware/Proxmox web interface rather than terminal commands.
# Part 1: Create hypervisor VMs and configure networking
# - Open VMware Workstation → File → New Virtual Machine.
# - Create at least two VMs to act as hypervisor hosts.
# - Install Proxmox VE on each VM, as specified in the lab.
# - Assign resources such as 2 CPUs and 8 GB RAM, subject to your computer's available resources.
# - Set each hypervisor VM's network adapter to Bridged mode.
# - Complete the installation and configure the IP address and root password on each hypervisor.
# - Open the Proxmox web interface for the first hypervisor and go to Datacenter → Cluster → Create Cluster.
# - Create the cluster and note the join information.
# - Open the second hypervisor's interface and use the cluster join option to join it to the first hypervisor.
# Part 2: Verify the cluster
# - Open the terminal or shell on each hypervisor.
# - Check connectivity between the nodes:
# ping SECOND_HYPERVISOR_IP
# Replace the IP with the second node's actual address. Press Ctrl + C to stop pinging.
# - Verify that both hypervisor nodes are visible in the Proxmox interface.
# Expected result: both nodes can communicate and appear in the same cluster.
# Part 3: Configure high availability (HA)
# - Open the cluster management interface.
# - Navigate to the High Availability settings.
# - Add or configure the VM that should restart on another host if its current host fails.
# - Power down one hypervisor host to test failover, then verify whether the configured VM restarts on another host.
# Note: automatic failover requires appropriate cluster configuration and storage accessible from the other node. A basic two-node setup may require additional quorum configuration.
# Part 4: Configure load balancing
# - Open the hypervisor management dashboard.
# - Configure resource distribution policies or thresholds if supported by your platform.
# - Run CPU- or memory-intensive workloads on VMs to simulate load.
# - Monitor CPU and memory usage in the dashboard and check whether workloads are redistributed.
# Part 5: Migrate VMs between hypervisors
# - Ensure the target hypervisor has compatible networking and access to the required VM storage.
# - Shut down the VM before manually migrating it.
# - Export the VM as an OVF template or copy its virtual disk files to the destination host.
# - Import the VM into the destination hypervisor and start it.
# - Verify that the VM boots, its services work and it has network connectivity.
# Expected result: a cluster with multiple hypervisor nodes, configured HA and resource distribution, plus a VM migration demonstration.