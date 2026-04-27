package com.transferapp.filetransfer.data

data class TransferItem(
    val id: Long = System.currentTimeMillis(),
    val type: ItemType,
    val fileName: String,
    val fileSize: Long = 0,
    val timestamp: Long = System.currentTimeMillis(),
    val status: TransferStatus = TransferStatus.SUCCESS
)

enum class ItemType {
    FILE, IMAGE, TEXT, LINK
}

enum class TransferStatus {
    SUCCESS, FAILED, PENDING
}

fun Long.formatFileSize(): String {
    return when {
        this < 1024 -> "$this B"
        this < 1024 * 1024 -> "${this / 1024} KB"
        this < 1024 * 1024 * 1024 -> "${this / (1024 * 1024)} MB"
        else -> "${this / (1024 * 1024 * 1024)} GB"
    }
}
