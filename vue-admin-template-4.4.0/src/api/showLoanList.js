import request from '@/utils/request'

export function showLoanList(data) {
    return request({
      url: '/api/',
      method: 'post',
      data
    })
}