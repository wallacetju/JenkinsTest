# -*- coding: utf-8 -*-

import StringIO
import sys
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

import HTMLTestRunner

# ----------------------------------------------------------------------

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

# ----------------------------------------------------------------------
# Sample tests to drive the HTMLTestRunner

class SampleTest0(unittest.TestCase):
    """ A class that passes.

    This simple class has only one test case that passes.
    """
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_pass_no_output(self):
        """        test description
        """
        pass

class SampleTest1(unittest.TestCase):
    """ A class that fails.

    This simple class has only one test case that fails.
    """
    def test_fail(self):
        """
        test description (描述)
        """
        self.fail()

class SampleOutputTestBase(unittest.TestCase):
    """ Base TestCase. Generates 4 test cases x different content type. """
    def test_1(self):
        print self.MESSAGE
    def test_2(self):
        print >>sys.stderr, self.MESSAGE
    def test_3(self):
        self.fail(self.MESSAGE)
    def test_4(self):
        raise RuntimeError(self.MESSAGE)

class SampleTestBasic(SampleOutputTestBase):
    MESSAGE = 'basic test'

class SampleTestHTML(SampleOutputTestBase):
    MESSAGE = 'the message is 5 symbols: <>&"\'\nplus the HTML entity string: [&copy;] on a second line'

class SampleTestLatin1(SampleOutputTestBase):
    MESSAGE = u'the message is áéíóú'.encode('latin-1')

class SampleTestUnicode(SampleOutputTestBase):
    u""" Unicode (統一碼) test """
    MESSAGE = u'the message is \u8563'
    # 2006-04-25 Note: Exception would show up as
    # AssertionError: <unprintable instance object>
    #
    # This seems to be limitation of traceback.format_exception()
    # Same result in standard unittest.
    def test_pass(self):
        u""" A test with Unicode (統一碼) docstring """
        pass


# ------------------------------------------------------------------------
# This is the main test on HTMLTestRunner

class Test_HTMLTestRunner(unittest.TestCase):

    def test0(self):
        self.suite = unittest.TestSuite()
        buf = StringIO.StringIO()
        runner = HTMLTestRunner.HTMLTestRunner(buf)
        runner.run(self.suite)
        # didn't blow up? ok.
        self.assert_('</html>' in buf.getvalue())

    def test_main(self):
        # Run HTMLTestRunner. Verify the HTML report.

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest0),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest1),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestBasic),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestHTML),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestLatin1),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestUnicode),
            ])

        # Invoke TestRunner
        buf = StringIO.StringIO()
        #runner = unittest.TextTestRunner(buf)       #DEBUG: this is the unittest baseline
        runner = HTMLTestRunner.HTMLTestRunner(
                    stream=buf,
                    title='<Demo Test>',
                    description='This demonstrates the report output by HTMLTestRunner.'
                    )
        runner.run(self.suite)

        # check out the output
        byte_output = buf.getvalue()
        # output the main test output for debugging & demo
        #print byte_output
        # HTMLTestRunner pumps UTF-8 output
        output = byte_output.decode('utf-8')
        # Write into html files
        with open('output.html', 'w') as f:
        	f.write(byte_output)

		me = "shuai.symantec@gmail.com"
		you = "shuai.symantec@gmail.com"
		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "Link"
		msg['From'] = me
		msg['To'] = you
		
		
		
		# PDF attachment
		filename='output.html'
		fp=open(filename,'r')
		att = MIMEApplication(fp.read(),_subtype="html")
		fp.close()
		att.add_header('Content-Disposition','attachment',filename=filename)
		msg.attach(att)
		
		
		
		
		# Send the message via local SMTP server.
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('shuai.symantec@gmail.com', 'Boston@001')
		mail.sendmail(me, you, msg.as_string())
		mail.quit()
		print 'successfully sent the mail'






##############################################################################
# Executing this module from the command line
##############################################################################

import unittest
if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv
    else:
        argv=['test_HTMLTestRunner.py', 'Test_HTMLTestRunner']
    unittest.main(argv=argv)
    # Testing HTMLTestRunner with HTMLTestRunner would work. But instead
    # we will use standard library's TextTestRunner to reduce the nesting
    # that may confuse people.
    #HTMLTestRunner.main(argv=argv)

