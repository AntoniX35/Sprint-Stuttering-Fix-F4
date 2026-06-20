#pragma once

#define WIN32_LEAN_AND_MEAN
#define NOMB
#define NOMINMAX
#define NOSERVICE

#pragma warning(push)
#include "F4SE/F4SE.h"
#include "RE/Fallout.h"

#include <spdlog/sinks/basic_file_sink.h>
#pragma warning(pop)

#define DLLEXPORT __declspec(dllexport)

namespace logger = F4SE::log;

using namespace std::literals;

namespace stl
{
	using namespace F4SE::stl;
}

#include "Version.h"
