package com.transferapp.filetransfer.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.transferapp.filetransfer.R
import com.transferapp.filetransfer.data.ItemType
import com.transferapp.filetransfer.data.TransferItem
import com.transferapp.filetransfer.data.formatFileSize
import com.transferapp.filetransfer.databinding.ItemHistoryBinding
import java.text.SimpleDateFormat
import java.util.*

class HistoryAdapter(
    private val items: List<TransferItem>,
    private val onItemClick: ((TransferItem) -> Unit)? = null
) : RecyclerView.Adapter<HistoryAdapter.HistoryViewHolder>() {

    class HistoryViewHolder(private val binding: ItemHistoryBinding) :
        RecyclerView.ViewHolder(binding.root) {
        
        fun bind(item: TransferItem, onItemClick: ((TransferItem) -> Unit)?) {
            binding.tvFileName.text = item.fileName
            
            // 设置类型标签
            val typeText = when (item.type) {
                ItemType.FILE -> "📁 文件"
                ItemType.IMAGE -> "🖼️ 图片"
                ItemType.TEXT -> "📝 文本"
                ItemType.LINK -> "🔗 链接"
            }
            binding.tvFileType.text = typeText
            
            // 设置文件大小
            if (item.fileSize > 0) {
                binding.tvFileName.text = "${item.fileName} (${item.fileSize.formatFileSize()})"
            }
            
            // 设置时间
            val dateFormat = SimpleDateFormat("MM-dd HH:mm", Locale.getDefault())
            binding.tvTime.text = dateFormat.format(Date(item.timestamp))
            
            // 设置图标
            val iconRes = when (item.type) {
                ItemType.FILE -> R.drawable.ic_file
                ItemType.IMAGE -> R.drawable.ic_image
                ItemType.TEXT -> R.drawable.ic_text
                ItemType.LINK -> R.drawable.ic_text
            }
            binding.ivIcon.setImageResource(iconRes)
            
            // 设置状态
            val statusRes = when (item.status) {
                TransferItem.TransferStatus.SUCCESS -> R.drawable.ic_success
                TransferItem.TransferStatus.FAILED -> R.drawable.ic_error
                TransferItem.TransferStatus.PENDING -> R.drawable.ic_file
            }
            binding.ivStatus.setImageResource(statusRes)
            
            // 点击事件
            binding.root.setOnClickListener {
                onItemClick?.invoke(item)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): HistoryViewHolder {
        val binding = ItemHistoryBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return HistoryViewHolder(binding)
    }

    override fun onBindViewHolder(holder: HistoryViewHolder, position: Int) {
        holder.bind(items[position], onItemClick)
    }

    override fun getItemCount(): Int = items.size
}
