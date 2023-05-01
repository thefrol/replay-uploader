import subprocess


def create_token():
    #take the first line and decode to string
    return subprocess.check_output('yc iam create-token').splitlines()[0].decode()
    #if error in yc? try parsing result codes with POPEN

#1)metadata hints https://cloud.yandex.ru/docs/compute/concepts/vm-metadata ssh and more
#2)put warning if no service acc specified, also warning if account has no docker-puller rights
def create_vm(
    name:str=None,
    zone='ru-central1-b',
    ssh_file=None,
    service_account_name=None,
    public_ip=False,
    container_name=None,
    container_image='cr.yandex.ru/mirror/ubuntu:16.04',
    container_command=None,
    container_arg=None,
    container_env=None,
    container_privileged=False,
    container_tty=False,
    container_stdin=False,
    container_restart_policy=None,
    preemptible=False,
    enable_serial_tty=False,
    memory=None,
    cores=None
    ):

    cmd="yc compute instance create-with-container"
    def append(str):
        nonlocal  cmd
        cmd=cmd+" "+str

    if name:
        append(f"--name {name}")
    if zone:
        append(f"--zone {zone}")
    if ssh_file:
        append(f"--ssh-key {ssh_file}")
    if service_account_name:
        append(f"--service-account-name {service_account_name}")
    if public_ip:
        append("--public-ip")
    if container_name:
        append(f"--container-name={container_name}")
    if container_image:
        append(f"--container-image={container_image}")
    if container_command:
        append(f"--container-command={container_command}")
    if container_arg:
        append(f"--container-arg={container_arg}")
    if memory:
        append(f'--memory {memory}')
    if cores:
        append(f'--cores {cores}')
    if container_env:
        env_string=""
        if isinstance(container_env,dict):
            for key in container_env:
                env_string=env_string+f"{key}={container_env[key]},"
            #deleta last comma
            env_string=env_string[:-1]
        else:
            env_string=container_env
        append(f"--container-env={env_string}")
    if container_privileged:
        append(f"--container-privileged")
    if container_tty:
        append(f"--container-tty")
    if container_stdin:
        append(f"--container-stdin")
    if preemptible:
        append(f"--preemptible")
    if container_restart_policy:
        append(f"--container-restart-policy={container_restart_policy}")

    #metadata
    
    metadata=''
    def add_metadata(data):
        nonlocal metadata
        metadata=metadata+data+" "
    if enable_serial_tty:
        add_metadata("serial-port-enable=1")
    if metadata!='':
        append(f'--metadata {metadata}')
    #if container_command:
    #    append(f"")
    subprocess.check_output(cmd)
    
#OK
#print(create_token())

#OK
#keys={'pp':'b',1:2}
#create_vm(
#    container_image='cr.yandex/crp477n9q5t5g1ho3ph3/higlights:beta2',
#    container_restart_policy='never',
#    container_env=keys,
#    service_account_name='docker-puller',# never forget
#    enable_serial_tty=True,
#    container_tty=True,
#    container_privileged=True,
#    container_stdin=True,
#    public_ip=True,
#    preemptible=True)

    
#kill public ip/tty/stdin/ssh
