import subprocess
import os

def get_build_flag():
    # --- MANUAL CONFIGURATION ZONE ---
    USE_MANUAL_VERSION = True 
    MANUAL_VERSION_NAME = "Nick Kay V1.4"
    # ---------------------------------

    if USE_MANUAL_VERSION:
        build_version = MANUAL_VERSION_NAME
        short_hash = "manual"
    else:
        # Original automated Git logic fallback
        ret = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, text=True)
        full_hash = ret.stdout.strip()
        ret = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], stdout=subprocess.PIPE, text=True)
        branch = ret.stdout.strip()
        short_hash = full_hash[:8]

        build_version = "local_" + branch + "_" + short_hash

        ref_name = os.environ.get('GITHUB_REF_NAME')
        if ref_name:
            if ref_name.startswith("v"):
                build_version = ref_name
            else:
                build_version = ref_name + "_" + short_hash

        ret = subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"], stdout=subprocess.PIPE, text=True)
        if ret.returncode != 0:
            build_version += "_modified"
            short_hash += "_modified"

    # Escaped quotes handle the spaces inside your custom name safely during compilation
    build_flags = f'-D BUILD_TAG=\\""{build_version}"\\" -D BUILD_HASH=\\""{short_hash}"\\"'

    return build_flags

build_flags = get_build_flag()

if "SCons.Script" == __name__:
    print ("Firmware Revision: " + build_flags)
    Import("env")
    env.Append(
        BUILD_FLAGS=[get_build_flag()]
    )
elif "__main__" == __name__:
    print(build_flags)