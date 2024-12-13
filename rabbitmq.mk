# ############
#   RabbitMQ
# ############
# Targets for managing a RabbitMQ message broker.

# Parameters used by the commands in the targets.
user=$(RABBITMQ_USER)
password=$(RABBITMQ_PASSWORD)
vhost=$(RABBITMQ_VHOST)

.PHONY: rabbitmq-clean
rabbitmq-clean:
	sudo rabbitmqctl delete_user $(user)
	sudo rabbitmqctl delete_vhost $(vhost)

.PHONY: rabbitmq-init
rabbitmq-init:
	sudo rabbitmqctl add_user $(user) $(password)
	sudo rabbitmqctl add_vhost $(vhost)
	sudo rabbitmqctl set_permissions --vhost $(vhost) $(user) ".*" ".*" ".*"
