#pragma once

#include <stk/cuda/stream.h>
#include <stk/image/gpu_volume.h>
#include <stk/image/volume.h>

#include "block_change_flags.h"
#include "settings.h"

#include <atomic>
#include <deque>
#include <mutex>

class GpuBinaryFunction;
class GpuUnaryFunction;
class WorkerPool;
class StreamPool;

// Hybrid (CPU-GPU) graph-cut optimizer.
//  Uses GPU to compute weights for graph and minimizes graph on CPU.
class HybridGraphCutOptimizer
{
public:
    HybridGraphCutOptimizer(
        const Settings::Level& settings,
        GpuUnaryFunction& unary_fn,
        GpuBinaryFunction& binary_fn,
        stk::GpuVolume& df,
        WorkerPool& worker_pool,
        std::vector<stk::cuda::Stream>& stream_pool
    );
    ~HybridGraphCutOptimizer();

    void execute();

private:
    struct Block
    {
        int3 idx;
        int3 begin;
        int3 end;
        bool shift;
    };

    // Allocates CPU and GPU buffers for the costs
    void allocate_cost_buffers(const dim3& size);

    // Sets the unary cost buffer to all zeros
    void reset_unary_cost();

    // Dispatches all queues block
    // Returns the number of changed blocks
    size_t dispatch_blocks();

    // Dispatches next cost block to specified stream (if any available in queue)
    void dispatch_next_cost_block(stk::cuda::Stream stream);

    // Dispatches a minimize block task
    void dispatch_minimize_block(const Block& block);

    // Applies delta based on labels in _gpu_labels.
    void apply_displacement_delta(stk::cuda::Stream stream);

    void download_subvolume(
        const stk::GpuVolume& src,
        stk::Volume& tgt,
        const Block& block,
        bool pad, // Pad all axes by 1 in negative direction for binary cost
        stk::cuda::Stream stream
    );

    void upload_subvolume(
        const stk::Volume& src,
        stk::GpuVolume& tgt,
        const Block& block,
        stk::cuda::Stream stream
    );

    // Calculates the energy sum for the given displacement field
    double calculate_energy();

    // Task that dispatches the computation of the block cost to the GPU.
    void block_cost_task(const Block& block, stk::cuda::Stream stream);

    // Performs graph cut on block
    // Returns true if block was changed
    void minimize_block_task(const Block& block);

    const Settings::Level& _settings;
    WorkerPool& _worker_pool;
    std::vector<stk::cuda::Stream>& _stream_pool;

    // Buffers for unary cost

    stk::VolumeFloat2 _unary_cost;
    stk::GpuVolume _gpu_unary_cost;

    // Buffers for binary cost

    stk::VolumeFloat4 _binary_cost_x;
    stk::VolumeFloat4 _binary_cost_y;
    stk::VolumeFloat4 _binary_cost_z;

    stk::GpuVolume _gpu_binary_cost_x;
    stk::GpuVolume _gpu_binary_cost_y;
    stk::GpuVolume _gpu_binary_cost_z;

    // Labels from the minimization

    stk::VolumeUChar _labels;
    stk::GpuVolume _gpu_labels;

    GpuUnaryFunction& _unary_fn;
    GpuBinaryFunction& _binary_fn;

    stk::GpuVolume _df;

    BlockChangeFlags _block_change_flags;
    std::atomic<size_t> _num_blocks_changed;
    std::atomic<size_t> _num_blocks_remaining;

    std::deque<Block> _block_queue;
    std::mutex _block_queue_lock;

    float3 _current_delta;

};
