import sys
import dbus_next.service
import dbus_next.aio
from dbus_next.service import Variant
from dbus_next.aio import MessageBus
from dbus_next import BusType
class Interact(dbus_next.service.ServiceInterface):
    DBUS_NAME = "com.puppy.Puppy"
    DBUS_PATH = "/com/puppy/Puppy/ShihTzu"
    DBUS_INTERFACE = "com.puppy.Puppy.ShihTzu"

    def __init__(self):
        super().__init__(self.DBUS_INTERFACE)

    # dst: destination for walk
    # time: how long it walks
    # range: how far it goes
    @dbus_next.service.method("WalkOutside")
    async def walk_outside(self, dst: "s", time: "n", range: "n", puppy: "v") -> "a{sv}":
        print()
        ret = dict()
        return ret
        
    @dbus_next.service.method("Feed")
    async def feed(self, amount: "n", puppy: "v") -> "b":
        print()
        ret = False
        return ret

    async def dbus_publish(self):
        try:
            bus = MessageBus(bus_type=BusType.SESSION)
            await bus.connect()
            bus.export("/com/puppy/Puppy/ShihTzu", self)
            await bus.request_name("com.puppy.Puppy")
            await bus.wait_for_disconnect()
        except Exception as e:
            print(e)
            sys.exit(1)

