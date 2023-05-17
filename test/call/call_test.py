import unittest
import time
from src.call.call import detail, post, live_enter, call_api, call_live_api, xiaohongshu_header


class CallTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xiaohongshu_cookies = [
            {
                'name': 'a1',
                'value': '188293a128980yj74fx4bior8rgkmagz1hvae47ot7350000155545',
            },
            {
                'name': 'web_session',
                'value': '030037a357fd6b55f18753ef1c234a7be23742',
            },
        ]

    def detail_assert(self, data):
        self.assertEqual(data['aweme_detail']['desc'], '#闺蜜 #姐妹 陪一个女孩长大 不如陪奶奶说说心里话')

    def post_assert(self, data):
        self.assertEqual(data['aweme_list'][0]['aweme_id'], '7209619920986885432')

    def call_live_api_assert(self, url: str):
        data = call_live_api(url)
        room_status: int = data['data']['room_status']
        self.assertEqual(room_status == 0 or room_status == 2, True)

    def test_detail(self):
        self.detail_assert(detail('7141964711570066722'))

    def test_post(self):
        self.post_assert(post("MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM", int(time.time() * 1_000)))

    def test_live_enter(self):
        data = live_enter('9409272172')
        room_status: int = data['data']['room_status']
        self.assertEqual(room_status == 0 or room_status == 2, True)

    def test_call_api_detail(self):
        self.detail_assert(call_api('https://www.douyin.com/video/7141964711570066722'))
        self.detail_assert(call_api('7141964711570066722'))

    def test_call_api_post(self):
        self.post_assert(
            call_api('https://www.douyin.com/user/MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'))
        self.post_assert(call_api('MS4wLjABAAAAc6-xMO2J77mP_3h_pOdPT-47qE0cywiTLB7PF4csqPM'))

    def test_call_api_share(self):
        self.detail_assert(call_api('https://v.douyin.com/kt5s7j4/'))
        data = call_api('https://v.douyin.com/StwKB7s/')
        self.assertEqual(data['aweme_detail']['desc'], '🌃🍂。#逆光拍照  #拉紧手跟我走')
        self.post_assert(call_api('https://v.douyin.com/kG3Cu1b/'))

    def test_call_live_api(self):
        self.call_live_api_assert('https://live.douyin.com/9409272172')
        self.call_live_api_assert('9409272172')

    def test_xiaohongshu_get_header(self):
        headers = xiaohongshu_header('/api/sns/web/v1/user_posted?num=30&cursor=&user_id=594099df82ec393174227f18',
                                     cookies=self.xiaohongshu_cookies)
        self.assertEqual(isinstance(headers['X-s'], str), True)
        self.assertEqual(isinstance(headers['X-t'], int), True)

    def test_xiaohongshu_post_header(self):
        headers = xiaohongshu_header('/api/sns/web/v1/feed',
                                     cookies=self.xiaohongshu_cookies,
                                     json={'source_note_id': '643df5670000000013003189'})
        self.assertEqual(isinstance(headers['X-s'], str), True)
        self.assertEqual(isinstance(headers['X-t'], int), True)


if __name__ == '__main__':
    unittest.main()
