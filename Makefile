TOP := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
TOOLS_DIR := $(TOP)tools
TWOLITER_DIR := $(TOOLS_DIR)/twoliter
TWOLITER := $(TWOLITER_DIR)/twoliter
CARGO_HOME := $(TOP).cargo

VARIANT ?= ootb-k8s-1.29

TWOLITER_VERSION ?= "0.4.6"
TWOLITER_SHA256_AARCH64 ?= "12ac3f5a6c641e29481c79289bd07cf1c3494a65e3d283d582feb1d28d8bf2a7"
TWOLITER_SHA256_X86_64 ?= "4a2db7c4d0aac75c6b682336539ee57371cfb6dfea81689d07fc1f4a940fd5c5"
UNAME_ARCH = $(shell uname -m)
ARCH ?= $(UNAME_ARCH)

ifeq ($(UNAME_ARCH), aarch64)
	TWOLITER_SHA256=$(TWOLITER_SHA256_AARCH64)
else
	TWOLITER_SHA256=$(TWOLITER_SHA256_X86_64)
endif

all: build

.PHONY: prep
prep:
	@mkdir -p $(TWOLITER_DIR)
	@mkdir -p $(CARGO_HOME)
	@$(TOOLS_DIR)/install-twoliter.sh \
		--repo "https://github.com/bottlerocket-os/twoliter" \
		--version v$(TWOLITER_VERSION) \
		--directory $(TWOLITER_DIR) \
		--reuse-existing-install \
		--allow-binary-install $(TWOLITER_SHA256) \
		--allow-from-source

.PHONY: update
update: prep
	@$(TWOLITER) update

.PHONY: fetch
fetch: prep
	@$(TWOLITER) fetch --arch $(ARCH)

.PHONY: build
build: fetch
	@$(TWOLITER) build variant $(VARIANT) --arch $(ARCH)

TWOLITER_MAKE = $(TWOLITER) make --cargo-home $(CARGO_HOME) --arch $(ARCH)

# Treat any targets after "make twoliter" as arguments to "twoliter make".
ifeq (twoliter,$(firstword $(MAKECMDGOALS)))
  TWOLITER_MAKE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(TWOLITER_MAKE_ARGS):;@:)
endif

# Transform "make twoliter" into "twoliter make", for access to tasks that are
# only available through the embedded Makefile.toml.
.PHONY: twoliter
twoliter: export BUILDSYS_VARIANT = $(VARIANT)
twoliter: prep
	@$(TWOLITER_MAKE) $(TWOLITER_MAKE_ARGS)