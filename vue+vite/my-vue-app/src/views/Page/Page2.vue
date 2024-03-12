<template>
<div class="demo-pagination-block">
<div class="demonstration">Change page size</div>
<el-pagination
    v-model:current-page="currentPage2"
    v-model:page-size="pageSize2"
    :page-sizes="[100, 200, 300, 400]"
    :small="small"
    :disabled="disabled"
    :background="background"
    layout="sizes, prev, pager, next"
    :total="1000"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
/>
</div>
</template>