from pvaccess import Channel
import pvaccess as pva


# Create a Channel object
c = Channel('MPS:TEL')

# Get the current value of the structure
current_value = c.get('field(action_counter)')
print(current_value)