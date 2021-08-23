from engine.models import VirtualMachine, FirewallRule


def get_tag_name(tags, text):
    for tag in tags:
        if tag.text == text:
            return text


def get_atackers(vm):
    vms = VirtualMachine.objects.all().exclude(vm_id=vm.vm_id)
    res = []
    ids = []
    for v in vms:
        for source_tag in v.tags.all():
            found = False
            for dest_tag in vm.tags.all():
                zz = FirewallRule.objects.filter(dest_tag=dest_tag, source_tag=source_tag)
                if zz:
                    res.append(f"{v.vm_id}->{v.name} ({get_tag_name(v.tags.all(), source_tag.text)})| {zz[0].fw_id} {source_tag.text}-{dest_tag.text} | {get_tag_name(vm.tags.all(), dest_tag.text)}")
                    ids.append(v.vm_id)
                    found = True
                    break
            if found:
                break
    return ', '.join(res), ids
