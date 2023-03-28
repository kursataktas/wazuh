#ifndef _API_METRICS_HANDLERS_HPP
#define _API_METRICS_HANDLERS_HPP

#include <api/registry.hpp>
#include "metrics.hpp"

namespace api::metrics::handlers
{
/**
 * @brief Dumps content of instruments.
 *
 * @return [api::CommandFn] Dumped data, or error message.
 */
api::Handler metricsDumpCmd();

/**
* @brief Get a specific instrument.
*
* @return [api::CommandFn] Instrument data, or error message.
*/
api::Handler metricsGetCmd();

/**
* @brief Enable or disable a specific instrument.
*
* @return [api::CommandFn] Returns "OK" if success, otherwise error message.
*/
api::Handler metricsEnableCmd();

/**
 * @brief List instruments.
 *
 * @return [api::CommandFn] Return the list of instruments.
 */
api::Handler metricsList();

/**
* @brief Generate a test instrument.
*
* @return [api::CommandFn] Returns "OK".
*/
api::Handler metricsTestCmd();

/**
 * @brief Register all available Metrics commands in the API registry.
 *
 * @param registry API registry.
 * @throw std::runtime_error If the command registration fails for any reason.
 */
void registerHandlers(std::shared_ptr<api::Registry> registry);

} // namespace api::metrics::handlers

#endif // _API_METRICS_HANDLERS_HPP
